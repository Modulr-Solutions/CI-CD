FROM python:3.12-slim AS builder
 
WORKDIR /build
 
# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && mkdir -p /install \
 && pip install --prefix=/install --ignore-installed -r requirements.txt
 
# Copier le code source
COPY app/ ./app/
COPY tests/ ./tests/
 
# Lancer les tests unitaires pendant le build
RUN pytest tests/ -v --tb=short
 
 
# -----
FROM python:3.12-slim AS runner
 
# Utilisateur non-root pour la sécurité
RUN useradd -m appuser
WORKDIR /app
USER appuser
 
# Copier uniquement les dépendances installées depuis le builder
COPY --from=builder /install /usr/local
 
# Copier le code de l'application
COPY --from=builder /build/app/ .
 
EXPOSE 5000
 
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"
 
CMD ["python", "app.py"]
 