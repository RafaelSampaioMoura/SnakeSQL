import streamlit as st
import pandas as pd
from SnakeSQL import abrir_conexao

# Configuração da página para um visual mais de "aplicativo"
st.set_page_config(page_title="SnakeIn - Rede Profissional", page_icon="💼", layout="wide")

# ==========================================
# CONEXÃO COM O BANCO
# ==========================================
@st.cache_resource
def get_conexao():
    try:
        return abrir_conexao()
    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        return None

conn = get_conexao()

if conn:
    # Cabeçalho da Rede Social
    col1, col2 = st.columns([1, 8])
    col1.title("🐍")
    col2.title("SnakeIn - Conectando Talentos")
    st.markdown("---")

    # Navegação Principal
    aba_feed, aba_perfil, aba_vagas, aba_admin = st.tabs([
        "🏠 Feed Geral (Select Avançado)", 
        "👤 Criar/Editar Perfil (Insert/Update)", 
        "🏢 Publicar Vaga (Insert)", 
        "⚙️ Explorador (Select Simples)"
    ])

    # ==========================================
    # ABA 1: FEED GERAL (Cruzamento de Dados / Select)
    # ==========================================
    with aba_feed:
        st.header("Profissionais em Destaque")
        st.write("Aqui cruzamos dados das tabelas `usuario`, `formacao` e `instituicao`.")
        
        cursor = conn.cursor()
        try:
            # JOIN para pegar o nome do usuário, o curso e a faculdade
            query_feed = """
                SELECT 
                    u.primeiro_nome || ' ' || u.ultimo_nome AS "Profissional",
                    u.sobre_mim AS "Resumo",
                    COALESCE(f.curso, 'Não informado') AS "Formação",
                    COALESCE(i.nome, 'Instituição não informada') AS "Instituição"
                FROM usuario u
                LEFT JOIN formacao f ON u.id = f.id_usuario
                LEFT JOIN instituicao i ON f.id_instituicao = i.id
                ORDER BY u.id DESC LIMIT 10;
            """
            cursor.execute(query_feed)
            dados_feed = cursor.fetchall()
            
            if dados_feed:
                for linha in dados_feed:
                    with st.container():
                        st.subheader(f"🎓 {linha[0]}")
                        st.caption(f"**Educação:** {linha[2]} | {linha[3]}")
                        st.write(f"_{linha[1]}_")
                        st.button("Conectar", key=f"btn_{linha[0]}")
                        st.divider()
            else:
                st.info("Nenhum profissional cadastrado ainda.")
        except Exception as e:
            st.error(f"Erro ao carregar o feed: {e}")

    # ==========================================
    # ABA 2: CRIAR E ATUALIZAR PERFIL (Insert / Update)
    # ==========================================
    with aba_perfil:
        col_cad, col_edit = st.columns(2)
        
        # INSERT: Novo Usuário
        with col_cad:
            st.subheader("Novo Cadastro")
            with st.form("form_novo_usuario"):
                nome = st.text_input("Primeiro Nome")
                sobrenome = st.text_input("Último Nome")
                sobre_mim = st.text_area("Sobre mim (Resumo Profissional)", placeholder="Ex: Apaixonado por Data Science, Python e integração de sistemas com Next.js...")
                
                submit_user = st.form_submit_button("Criar Perfil")
                if submit_user:
                    try:
                        cursor.execute(
                            "INSERT INTO usuario (primeiro_nome, ultimo_nome, sobre_mim) VALUES (%s, %s, %s)",
                            (nome, sobrenome, sobre_mim)
                        )
                        conn.commit()
                        st.success(f"Bem-vindo(a) ao SnakeIn, {nome}!")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Erro ao cadastrar: {e}")

        # UPDATE: Editar "Sobre mim"
        with col_edit:
            st.subheader("Atualizar Perfil")
            with st.form("form_atualizar_usuario"):
                id_usuario = st.number_input("Seu ID de Usuário", min_value=1, step=1)
                novo_sobre = st.text_area("Novo Resumo Profissional")
                
                submit_update = st.form_submit_button("Atualizar Resumo")
                if submit_update:
                    try:
                        cursor.execute(
                            "UPDATE usuario SET sobre_mim = %s WHERE id = %s",
                            (novo_sobre, id_usuario)
                        )
                        conn.commit()
                        if cursor.rowcount > 0:
                            st.success("Perfil atualizado com sucesso! Atualize a página para ver no Feed.")
                        else:
                            st.warning("Usuário não encontrado.")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Erro ao atualizar: {e}")

    # ==========================================
    # ABA 3: PUBLICAR VAGA (Insert)
    # ==========================================
    with aba_vagas:
        st.header("Área de Recrutadores")
        st.write("Adicione uma nova oportunidade na tabela `cargo`.")
        
        with st.form("form_nova_vaga"):
            nome_vaga = st.text_input("Título da Vaga", placeholder="Ex: Engenheiro de Dados Júnior")
            nome_empresa = st.text_input("Empresa", placeholder="Ex: Tech Soluções")
            salario = st.number_input("Salário Oferecido (R$)", min_value=0.0, format="%.2f")
            desc_vaga = st.text_area("Descrição e Requisitos", placeholder="Ex: Necessário conhecimento em Python, SQL e modelagem de banco de dados...")
            
            submit_vaga = st.form_submit_button("Publicar Vaga")
            if submit_vaga:
                try:
                    cursor.execute(
                        "INSERT INTO cargo (nome, empresa, salario, descricao) VALUES (%s, %s, %s, %s)",
                        (nome_vaga, nome_empresa, salario, desc_vaga)
                    )
                    conn.commit()
                    st.success("Oportunidade publicada com sucesso!")
                except Exception as e:
                    conn.rollback()
                    st.error(f"Erro ao publicar vaga: {e}")

    # ==========================================
    # ABA 4: EXPLORADOR ADMIN (Select Dinâmico)
    # ==========================================
    with aba_admin:
        st.header("Visão do Banco de Dados")
        todas_tabelas = ["usuario", "cargo", "empresa", "formacao", "experiencia_profissional", "instituicao", "endereco", "contato"]
        tabela_selecionada = st.selectbox("Selecione a tabela para inspecionar:", todas_tabelas)
        
        if st.button("Carregar Dados Brutos"):
            try:
                cursor.execute(f"SELECT * FROM {tabela_selecionada} LIMIT 50;")
                dados_brutos = cursor.fetchall()
                if dados_brutos:
                    colunas = [desc[0] for desc in cursor.description]
                    df = pd.DataFrame(dados_brutos, columns=colunas)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Tabela vazia.")
            except Exception as e:
                st.error(f"Erro na consulta: {e}")

    # Fecha o cursor ao final da execução da página
    if 'cursor' in locals():
        cursor.close()