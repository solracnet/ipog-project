from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(model=Groq(id="llama-3.3-70b-versatile"), markdown=True)

def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)

def check_null_values(df: pd.DataFrame) -> None:
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print("Null values found:")
        print(null_counts[null_counts > 0])
    else:
        print("No null values found.")

def calculate_sales_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['Total_Sale'] = df['Sales'] * df['Quantity']
    df['Total_Sale_After_Discount'] = df['Total_Sale'] - df['Discount']
    return df


# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    data = load_data("./data/SampleSuperstore.csv")
    check_null_values(data)
    data = calculate_sales_metrics(data)

    print(data.head())
    # user_prompt = input("Digite sua pergunta: ")

    # --- Sync + Streaming ---
    # agent.print_response(user_prompt, stream=True)