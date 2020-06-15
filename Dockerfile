FROM python:3.8-buster

# See https://code.visualstudio.com/docs/remote/containers-advanced#_creating-a-nonroot-user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME
USER $USERNAME

WORKDIR /home/${USERNAME}

# Dependencies
COPY requirements.txt .
COPY requirements/ ./requirements/
RUN pip install -r requirements.txt

# Dev dependencies
ARG DEV=false
RUN if [ ${DEV} = "true" ]; then \
    pip install -r requirements/dev.txt; \
    fi

# Project
COPY app .
CMD ["python", "-m", "app"]