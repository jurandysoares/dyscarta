import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from dotenv import dotenv_values
import markdown
import typer

smtp_conf = dotenv_values(".env")

def oi():#nome: str, ano_nasc: int, verboso: bool = False):
    print(f"Olá.")
    print("Seja bem-vindo(a) ao sistema dyscarta!")

def envia_correspondencia(para: list[str], assunto: str, corpo_markdown: str, arquivos: list[str] = []):
    """
    Envia um e-mail através de um servidor SMTP, utilizando conexão segura (TLS).
    O corpo da mensagem é convertido de Markdown para HTML.

    Args:
        para (list[str]): Lista de endereços de e-mail dos destinatários.
        assunto (str): O assunto do e-mail.
        corpo_markdown (str): O conteúdo do corpo do e-mail no formato Markdown.
        arquivos (list[str], optional): Lista de caminhos para os arquivos a serem anexados. Padrão é [].
    """
    # 1. Extração das credenciais do arquivo .env
    SMTP_SERVER = smtp_conf["SMTP_SERVER"]
    SMTP_PORT = smtp_conf["SMTP_PORT"]
    SMTP_USER = smtp_conf["SMTP_USER"]
    SMTP_PASSWORD = smtp_conf["SMTP_PASSWORD"]
    
    remetente = SMTP_USER 

    if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD]):
        print("Erro: As variáveis SMTP (SERVER, PORT, USER, PASSWORD) não foram carregadas corretamente do .env.")
        return
        
    # --- NOVIDADE: Conversão de Markdown para HTML ---
    # Converte o texto Markdown em HTML, o que permite o uso de formatação
    corpo_html = markdown.markdown(corpo_markdown)
    
    # 2. Criação da Mensagem
    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = ", ".join(para) 
    msg['Subject'] = assunto
    
    # Anexa o corpo do e-mail no formato HTML
    msg.attach(MIMEText(corpo_html, 'html')) 

    # 3. Anexos (Lógica mantida igual)
    for caminho_arquivo in arquivos:
        try:
            parte = MIMEBase('application', 'octet-stream')
            with open(caminho_arquivo, 'rb') as file:
                parte.set_payload(file.read())
            
            encoders.encode_base64(parte)
            
            nome_arquivo = os.path.basename(caminho_arquivo)
            parte.add_header(
                'Content-Disposition',
                f'attachment; filename="{nome_arquivo}"',
            )
            
            msg.attach(parte)
            
        except FileNotFoundError:
            print(f"Aviso: Arquivo de anexo não encontrado: {caminho_arquivo}")
        except Exception as e:
            print(f"Erro ao anexar o arquivo {caminho_arquivo}: {e}")

    # 4. Envio do E-mail com TLS (Lógica mantida igual)
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            
            texto = msg.as_string()
            server.sendmail(remetente, para, texto)
            
        print(f"✅ E-mail enviado com sucesso para: {', '.join(para)}")

    except smtplib.SMTPAuthenticationError:
        print("❌ Erro de Autenticação: Verifique o usuário e a senha no arquivo .env.")
    except smtplib.SMTPConnectError:
        print("❌ Erro de Conexão: Verifique o servidor e a porta SMTP no arquivo .env.")
    except Exception as e:
        print(f"❌ Ocorreu um erro inesperado durante o envio: {e}")