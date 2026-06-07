# 🚀 Documentação e Guia de Deploy - Pedreiras FC

Este documento contém as instruções fundamentais para a manutenção e atualização das aplicações do **Painel Financeiro** e **Torneio** hospedadas na VPS (Servidor). Guarde este guia para consultar sempre que for trabalhar em um novo computador.

## 🧠 Lógica do Sistema e Arquitetura

O ecossistema do Pedreiras FC roda no servidor VPS utilizando a tecnologia **Docker Swarm**.

- **Traefik (Roteador)**: Atua como o "porteiro" da rede. Ele recebe todos os acessos do `pedreirasfc.com.br` e direciona os visitantes corretamente para os subdiretórios `/financeiro/` e `/torneio/`.
- **Containers Docker**: Cada sistema (Financeiro, Torneio, Portal Principal) roda em um ambiente isolado e protegido chamado container.
- **A Imagem Base (`pedreiras-app:latest`)**: É como se fosse um pendrive fechado contendo todo o seu código (`.py`, `.html`) e as instalações do Python (`requirements.txt`). Os containers "nascem" a partir desta imagem.
- **Comunicação com o Google Sheets**: As aplicações consomem os dados das planilhas em formato `.csv`. O Streamlit utiliza um sistema de **cache** (memória rápida) para evitar congestionar a planilha a cada segundo. Se você editar a planilha, o app pode segurar a informação velha por um tempo — por isso foi criado o botão "🔄 Atualizar Dados" na barra lateral das aplicações.

---

## 🔄 Como Atualizar as Aplicações na VPS (O Fluxo de Trabalho)

Sempre que você alterar o código no seu computador (Visual Studio Code, etc) e fizer o envio (Commit / Push) para o GitHub, você **precisa** entrar na VPS via SSH (Termius) e executar as 3 etapas abaixo.

### Passo 1: Puxar o código novo do GitHub
```bash
cd ~/dashboard-pedreiras-fc
git pull
```
*Isso faz a pasta do servidor baixar os arquivos de texto mais recentes.*

### Passo 2: Reconstruir a Imagem Docker (Obrigatório)
```bash
docker build -t pedreiras-app:latest .
```
*Como as aplicações rodam baseadas em uma imagem fechada, esse comando "injeta" as novidades do Passo 1 para dentro de uma nova imagem. Se pular este passo, o sistema continuará rodando com o código velho!*

> **⚠️ Dica de Ouro:** Se você precisou adicionar ou remover pacotes do `requirements.txt`, ou mexeu na receita estrutural do `Dockerfile`, você deve forçar o Docker a não usar atalhos adicionando o comando `--no-cache`:
> `docker build --no-cache -t pedreiras-app:latest .`

### Passo 3: Reiniciar os Serviços (Aplicar a mudança ao vivo)
Agora que a imagem nova está pronta, reinicie os sistemas afetados pela sua mudança:

**Atualizar o Torneio:**
```bash
docker service update --force pedreiras_torneio
```

**Atualizar o Financeiro:**
```bash
docker service update --force pedreiras_financeiro
```

**Atualizar a Tela Inicial (Portal):**
```bash
docker service update --force pedreiras_portal
```

---

## 🛠️ Outros Comandos Úteis

**1. Ver se os sistemas estão rodando ("running") ou caindo ("failed"):**
```bash
docker service ls
```

**2. Ler os logs (mensagens de erro do código python) de um serviço:**
```bash
docker service logs pedreiras_financeiro --tail 50 -f
```
*(Para sair da tela de logs, aperte `Ctrl + C`)*

**3. Quando eu devo usar o Portainer Web?**
Se as suas alterações de código envolveram mudar o arquivo de rotas e configurações profundas chamado `swarm-stack.yml`, o `git pull` não basta. Você precisará abrir o painel WEB do Portainer > aba Stacks > abrir a stack "pedreiras" > aba Editor > clicar no botão **"Update the stack"**.

---

## 🛑 Resumo de Resolução de Problemas

- **"Mudei o código, mandei pro Github, mas o site não mudou!"**
  *Diagnóstico:* Você pulou o **Passo 2** ou o **Passo 3**. Faça o `docker build` e em seguida o `docker service update`.
  
- **"Editei a planilha do torneio e a classificação não mexeu!"**
  *Diagnóstico:* O sistema cacheou a planilha. Vá na aba lateral do sistema na web e clique no botão **"🔄 Atualizar Dados"**.
