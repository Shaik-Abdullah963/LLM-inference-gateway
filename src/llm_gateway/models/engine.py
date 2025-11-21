"""Model inference engine with support for text generation."""

import time
from typing import Optional, AsyncIterator
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer
from threading import Thread

from llm_gateway.core.config import config
from llm_gateway.utils import get_logger, model_info, tokens_generated, generation_duration

logger = get_logger(__name__)


class InferenceEngine:
    """Manages model loading and inference operations."""
    
    def __init__(self):
        """Initialize the inference engine."""
        self.model = None
        self.tokenizer = None
        self.device = config.model.device
        self._is_loaded = False
    
    def load_model(self):
        """Load the model and tokenizer."""
        if self._is_loaded:
            logger.info("Model already loaded", model=config.model.model_name)
            return
        
        logger.info(
            "Loading model",
            model_name=config.model.model_name,
            device=self.device
        )
        
        try:
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                config.model.model_name,
                cache_dir=config.model.model_cache_dir,
            )
            
            # Set padding token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                config.model.model_name,
                cache_dir=config.model.model_cache_dir,
                torch_dtype=torch.float32 if self.device == "cpu" else torch.float16,
            )
            
            self.model.to(self.device)
            self.model.eval()
            
            # Update metrics
            model_info.info({
                "name": config.model.model_name,
                "device": self.device,
            })
            
            self._is_loaded = True
            logger.info("Model loaded successfully", model=config.model.model_name)
            
        except Exception as e:
            logger.error("Failed to load model", error=str(e))
            raise
    
    def generate(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
    ) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            
        Returns:
            Generated text
        """
        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Use config defaults if not specified
        max_length = max_length or config.model.max_length
        temperature = temperature or config.model.temperature
        top_p = top_p or config.model.top_p
        top_k = top_k or config.model.top_k
        
        start_time = time.time()
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    temperature=temperature,
                    top_p=top_p,
                    top_k=top_k,
                    do_sample=temperature > 0,
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            
            # Decode output
            generated_text = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
            
            # Update metrics
            num_tokens = outputs[0].shape[0] - inputs.input_ids.shape[1]
            tokens_generated.inc(num_tokens)
            generation_duration.observe(time.time() - start_time)
            
            logger.info(
                "Generated text",
                prompt_length=len(prompt),
                output_length=len(generated_text),
                tokens=num_tokens,
                duration=time.time() - start_time,
            )
            
            return generated_text
            
        except Exception as e:
            logger.error("Generation failed", error=str(e))
            raise
    
    async def generate_stream(
        self,
        prompt: str,
        max_length: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        top_k: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        Generate text from a prompt with streaming output.
        
        Args:
            prompt: Input text prompt
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            
        Yields:
            Generated text chunks
        """
        if not self._is_loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        # Use config defaults if not specified
        max_length = max_length or config.model.max_length
        temperature = temperature or config.model.temperature
        top_p = top_p or config.model.top_p
        top_k = top_k or config.model.top_k
        
        start_time = time.time()
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
            ).to(self.device)
            
            # Setup streaming
            streamer = TextIteratorStreamer(
                self.tokenizer,
                skip_special_tokens=True,
                skip_prompt=True
            )
            
            # Generation kwargs
            generation_kwargs = {
                **inputs,
                "max_length": max_length,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "do_sample": temperature > 0,
                "pad_token_id": self.tokenizer.pad_token_id,
                "eos_token_id": self.tokenizer.eos_token_id,
                "streamer": streamer,
            }
            
            # Run generation in a separate thread
            generation_output = {"num_tokens": 0}
            exception_holder = {"exception": None}
            
            def generate_with_exception_handling():
                """Wrapper to catch exceptions in generation thread."""
                try:
                    self.model.generate(**generation_kwargs)
                except Exception as e:
                    exception_holder["exception"] = e
            
            thread = Thread(target=generate_with_exception_handling)
            thread.start()
            
            # Stream the output
            generated_text = ""
            for text in streamer:
                generated_text += text
                yield text
            
            thread.join()
            
            # Check for exceptions in generation thread
            if exception_holder["exception"]:
                raise exception_holder["exception"]
            
            # Count actual tokens from generated text
            num_tokens = len(self.tokenizer.encode(generated_text))
            
            # Update metrics
            tokens_generated.inc(num_tokens)
            generation_duration.observe(time.time() - start_time)
            
            logger.info(
                "Streamed generation complete",
                prompt_length=len(prompt),
                tokens=num_tokens,
                duration=time.time() - start_time,
            )
            
        except Exception as e:
            logger.error("Streaming generation failed", error=str(e))
            raise
    
    def unload_model(self):
        """Unload the model to free memory."""
        if self._is_loaded:
            logger.info("Unloading model")
            self.model = None
            self.tokenizer = None
            self._is_loaded = False
            if torch.cuda.is_available():
                torch.cuda.empty_cache()


# Global inference engine instance
engine = InferenceEngine()
