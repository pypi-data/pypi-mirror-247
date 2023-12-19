import os
from os import getenv

from kink import di
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import AzureOpenAI, GPT4All, OpenAI, VertexAI


def bootstrap():
    di["embedding_model"] = getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    di["index_schema"] = getenv("INDEX_SCHEMA", "/tmp/redis_schema.yaml")
    di["redis_url"] = getenv("REDIS_URL", "redis://localhost:6379")
    di["vectorstore_name"] = getenv("VECTORSTORE_NAME", "faiss")
    di["vectorstore_path"] = getenv("VECTORSTORE_PATH", "/tmp/vectorstore")

    di["deployment_name"] = getenv("DEPLOYMENT_NAME", "text")
    di["model_name"] = getenv("MODEL_NAME", "text-bison@001")
    di["n"] = int(getenv("N", "1"))
    di["stop"] = getenv("STOP", None)
    di["max_output_tokens"] = int(getenv("MAX_OUTPUT_TOKENS", "1024"))
    di["temperature"] = float(getenv("TEMPERATURE", "0.1"))
    di["top_p"] = float(getenv("TOP_P", "0.8"))
    di["top_k"] = int(getenv("TOP_K", "40"))
    di["verbose"] = True

    di["vertex_ai"] = lambda di: VertexAI(
        model_name=di["model_name"],
        n=di["n"],
        stop=di["stop"],
        max_output_tokens=di["max_output_tokens"],
        temperature=di["temperature"],
        top_p=di["top_p"],
        top_k=di["top_k"],
        verbose=di["verbose"],
    )

    MODEL_PATH = getenv("GPT4ALL_MODEL_PATH", os.getcwd() + "/models/orca-mini-3b-gguf2-q4_0.gguf")
    isExist = os.path.exists(MODEL_PATH)
    if isExist:
        di["gpt4all_model_path"] = MODEL_PATH

        di["gpt4all"] = lambda di: GPT4All(
            model=di["gpt4all_model_path"],
            backend="gptj",
            callbacks=[StreamingStdOutCallbackHandler()],
            verbose=True
        )
    else:
        di["gpt4all"] = None

    di["openai"] = lambda di: OpenAI(
        model=di["model_name"],
        temperature=di["temperature"],
    )

    di["azure_openai"] = lambda di: AzureOpenAI(
        deployment_name=di["deployment_name"],
        model_name=di["model_name"],
    )

    di["rag_chain_main_llm"] = di["gpt4all"]
    di["rag_chain_clinical_llm"] = di["gpt4all"]
    di["fhir_agent_llm"] = di["gpt4all"]
    di["self_gen_cot_llm"] = di["gpt4all"]

    # Should be last
    from .tools import GetMedicalRecordTool
    from .utils import HapiFhirServer
    di["fhir_server"] = HapiFhirServer()
    di["patient_id"] = getenv("PATIENT_ID", "592911")
    di["get_medical_record_tool"] = GetMedicalRecordTool()
