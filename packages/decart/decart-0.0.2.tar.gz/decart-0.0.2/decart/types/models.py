import enum


class Model(str, enum.Enum):

    LLAMA_70B_CHAT = "meta-llama/llama-2-70b-chat-hf"

    MISTRAL_7B_INSTRUCT = "mistralai/mistral-7b-instruct-v0.1"

    ZEPHYR_7B_BETA = "huggingfaceh4/zephyr-7b-beta"

    LZLV_70B = "lizpreciatior/lzlv_70b_fp16_hf"

    FALCON_180B = "tiiuae/falcon-180b-chat"
