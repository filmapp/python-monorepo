FROM python:3.11-bullseye
RUN pip install --upgrade pip poetry

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    shellcheck \
    tree

# Create user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -s /bin/bash --uid ${USER_UID} --gid ${USERNAME} -m ${USERNAME} -p ''
ENV PATH=/home/vscode/.local/bin:$PATH

# VSCode extension
ARG USERNAME=vscode
RUN mkdir -p /home/$USERNAME/.vscode-server/extensions \
    /home/$USERNAME/.vscode-server-insiders/extensions \
    && chown -R ${USERNAME}:${USERNAME} \
    /home/$USERNAME/.vscode-server \
    /home/$USERNAME/.vscode-server-insiders

# Bash History
ARG USERNAME=vscode
RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" \
    && mkdir /commandhistory \
    && touch /commandhistory/.bash_history \
    && chown -R ${USERNAME}:${USERNAME} /commandhistory \
    && echo $SNIPPET >> "/home/$USERNAME/.bashrc" \
    && echo $SNIPPET >> "/home/$USERNAME/.zshrc"
