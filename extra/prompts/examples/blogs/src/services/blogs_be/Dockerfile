FROM blogs_base_python

# Run pre-install scripts
COPY install_scripts/install-postgres-tools.sh /app/install_scripts/
RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    bash /app/install_scripts/install-postgres-tools.sh

# Copy each library
COPY libs/jazzoo /app/libs/jazzoo
COPY libs/woodstock /app/libs/woodstock

# Install the service
COPY services/blogs_be /app/src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system --break-system-packages -e /app/src -r /app/src/requirements.txt

WORKDIR /app/src
