import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

# Import for A/B testing
from deliverables.part2_ab_testing.lib.experiments_client import ExperimentsClient

load_dotenv()


class GeneralResponse(BaseModel):
    reasoning: str = Field(..., description="Brief reasoning for the response. Max 20 words.")
    respuesta_final: str = Field(..., description="Response to the user in Colombian Spanish.")


# Important: This part was operated on to perform the AB Test
# Original Prompt (Control)
GENERAL_SYSTEM_PROMPT = """\
You are Emporyum Tech's virtual assistant. Emporyum Tech is a Colombian e-commerce platform \
that offers buy-now-pay-later installment plans.

## USER DATA
{user_data}

## KNOWLEDGE BASE
{knowledge_base}

## RULES
- ALWAYS address the user by their first name (primer_nombre).
- When asked about products, reference their category preferences and available promotions.
- When asked about orders, reference their specific orders (product name, status, amounts).
- When asked about payments, reference their outstanding balances and installment details.
- Respond in natural Colombian Spanish, 2-4 sentences.
- If you don't have enough information to answer, say so honestly."""

# Prompt optimized for AB Test (Variant A)
GENERAL_SYSTEM_PROMPT_TEST = """\### ROLE AND PERSONALITY
Act as the official Artificial Intelligence for Emporyum Tech. 
Your personality is professional, approachable, and efficient. 
Use a natural Colombian Spanish tone (standard/neutral, avoiding extreme regionalisms while maintaining local warmth).

### OPERATIONAL CONTEXT
Emporyum Tech is a leading Colombian e-commerce platform that facilitates access to technology and consumer goods through the "Buy Now, Pay Later" (BNPL) model. Your goal is to resolve inquiries regarding the product catalog and the user's financial status swiftly.

### INPUT VARIABLES
- **USER DATA:** {user_data}
- **KNOWLEDGE BASE:** {knowledge_base}

### RESPONSE PROTOCOL (STRICT RULES)
1. **Mandatory Personalization:** Always begin by greeting the user by their {primer_nombre}.
2. **Product Inquiries:** Cross-reference the user's intent with their {categorias_preferidas} and highlight {promociones_vigentes} if they are relevant. Do not list random products.
3. **Order Management:** When discussing orders, specify the {nombre_producto}, {estado_envio}, and {valor_total} to build trust.
4. **Financial Clarity:** If payments are mentioned, detail the {saldo_pendiente} and the value of the {proxima_cuota} with exact dates.
5. **Conciseness:** Keep the response between 2 and 4 sentences. Deliver value directly without filler.
6. **Data Honesty:** If the requested information is not present in {user_data} or {knowledge_base}, state honestly that you do not have access to that specific detail and offer to escalate the inquiry to a human agent.

### CONSTRAINTS
- DO NOT hallucinate account balances or delivery dates.
- DO NOT use complex technical terminology regarding interest rates unless explicitly asked.
- DO NOT switch inconsistently between "tú" and "usted"; maintain a friendly yet respectful "tú" unless the user data dictates otherwise.
"""


general_prompt_control = ChatPromptTemplate.from_messages([
    ("system", GENERAL_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])

general_prompt_test = ChatPromptTemplate.from_messages([
    ("system", GENERAL_SYSTEM_PROMPT_TEST),
    MessagesPlaceholder(variable_name="messages"),
    ("human", "{question}"),
])

def get_variant_config(user_id: str = None):
    """Determine the prompt variant for a given user ID using the experiment service."""
     # A/B testing logic
    if user_id:
        try:
            client = ExperimentsClient(os.getenv("EXPERIMENTS_API_URL"))
            variant = client.get_variant(os.getenv("EXPERIMENTS_ID"), user_id)
            prompt = general_prompt_test if variant["name"] == "test" else general_prompt_control
        except Exception as e:
            # Fallback to control if experiment service is not available
            print(f"[WARNING] Experiment service unavailable: {e}. Using control prompt.")
            prompt = general_prompt_control
    else:
        prompt = general_prompt_control
    return prompt

def get_general_chain(user_id: str = None):
    """Build and return the general agent chain with structured output."""
    prompt = get_variant_config(user_id)
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return prompt | llm.with_structured_output(GeneralResponse)
