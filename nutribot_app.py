import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="NutriBot", page_icon="💪", layout="centered")

# 🏷️ Cabeçalho
st.image("https://i.imgur.com/0XjKX9z.png", width=200)
st.title("NutriBot 💬")
st.subheader("Seu assistente de treino e nutrição personalizado")

# 📝 Coleta de dados
objetivo = st.selectbox("Qual é o seu objetivo?", ["Ganhar massa muscular", "Emagrecer", "Saúde geral"])
local = st.radio("Onde você prefere treinar?", ["Em casa", "Na academia"])
dias_livres = st.multiselect(
    "Quais dias da semana você tem disponíveis para treinar?",
    ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
)

# 📋 Sugestão de treino com lógica simulada de IA
def gerar_treino(objetivo, local, dias_livres):
    dias = len(dias_livres)
    if objetivo == "Ganhar massa muscular":
        if local == "Em casa":
            plano = f"Plano de {dias} dias com exercícios como flexões, agachamentos, prancha e elásticos."
        else:
            plano = f"Plano de {dias} dias com musculação dividida por grupos musculares."
    elif objetivo == "Emagrecer":
        plano = f"Plano de {dias} dias com foco em HIIT, cardio e mobilidade."
    else:
        plano = f"Plano leve de {dias} dias com caminhada, alongamento e exercícios funcionais."

    sugestao = f"Recomendo treinar nos dias: {', '.join(dias_livres)}. Mantenha consistência e descanso adequado."
    return plano + "\n\n" + sugestao

# 🍽️ Dica nutricional
def dica_nutricional(objetivo):
    if objetivo == "Ganhar massa muscular":
        return "🍗 Consuma proteínas magras, carboidratos complexos e mantenha boa hidratação."
    elif objetivo == "Emagrecer":
        return "🥗 Priorize vegetais, evite açúcares simples e mantenha um déficit calórico saudável."
    else:
        return "🍎 Mantenha uma dieta equilibrada com frutas, legumes e gorduras boas."

# 📊 Gráfico de treino semanal
def gerar_grafico(dias_livres):
    fig, ax = plt.subplots()
    semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    treino = [1 if dia in dias_livres else 0 for dia in semana]
    ax.bar(semana, treino, color="green")
    ax.set_title("Distribuição semanal de treinos")
    return fig

# ▶️ Botão de geração
if st.button("Gerar plano personalizado"):
    if dias_livres:
        st.success("✅ Seu plano está pronto!")
        st.write("📋 Plano de treino:")
        st.write(gerar_treino(objetivo, local, dias_livres))
        st.write("🍽️ Dica nutricional:")
        st.write(dica_nutricional(objetivo))
        st.pyplot(gerar_grafico(dias_livres))
        st.info("📄 Em breve: geração de PDF com seu plano completo.")
    else:
        st.warning("⚠️ Por favor, selecione ao menos um dia da semana disponível para treinar.")
from fpdf import FPDF

def gerar_pdf(objetivo, local, dias_livres, plano, dica):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Plano Personalizado - NutriBot", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Objetivo: {objetivo}", ln=True)
    pdf.cell(200, 10, txt=f"Local de treino: {local}", ln=True)
    pdf.cell(200, 10, txt=f"Dias disponíveis: {', '.join(dias_livres)}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Plano de treino:\n{plano}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Dica nutricional:\n{dica}")

    pdf.output("plano_nutribot.pdf")
if st.button("📄 Baixar plano em PDF"):
    plano = gerar_treino(objetivo, local, dias_livres)
    dica = dica_nutricional(objetivo)
    gerar_pdf(objetivo, local, dias_livres, plano, dica)
    st.success("✅ PDF gerado com sucesso! Verifique o arquivo 'plano_nutribot.pdf' na sua pasta.")
import requests

def responder_cometapi(pergunta, chave_api):
    url = "https://api.cometapi.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {chave_api}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "google/gemini-pro",  # Você pode trocar por outro modelo da CometAPI
        "messages": [
            {"role": "system", "content": "Você é um especialista em nutrição e treino. Responda de forma clara e prática."},
            {"role": "user", "content": pergunta}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Erro {response.status_code}: {response.text}"

# 🔐 Sua chave da CometAPI
chave_comet = "sk-tfIzqx74SkixaF5lppMOd0KzPPpKMNzkbvtzQXStMrN5E6Zp"  # Substitua pela sua chave real

# 🧠 Interface de perguntas com IA
st.subheader("❓ Pergunte ao NutriBot com IA")
pergunta = st.text_input("Digite sua dúvida sobre treino ou alimentação:")

if st.button("Responder com IA"):
    if pergunta:
        with st.spinner("Pensando..."):
            resposta = responder_cometapi(pergunta, chave_comet)
        st.success("💬 Resposta do NutriBot:")
        st.write(resposta)
    else:
        st.warning("⚠️ Digite uma pergunta antes de clicar.")

