# 🚀 Crypto Trading System

Sistema automatizado de trading de criptomonedas que integra análisis de sentimiento de X (Twitter) con ejecución de operaciones en Uniswap.

## 📋 Descripción General

Este sistema combina 4 componentes principales para realizar trading algorítmico de criptomonedas:

1. **Motor de Trading Uniswap** - Ejecución de órdenes de compra/venta en Uniswap
2. **Seguimiento de X** - Monitoreo de cuentas influyentes de Twitter/X
3. **Análisis de Señales** - Procesamiento NLP y detección de tendencias
4. **Motor de Decisiones** - Estrategias de trading y gestión de riesgo

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     API Layer (REST)                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ↓                     ↓                     ↓
┌───────────────┐   ┌──────────────────┐   ┌──────────────┐
│   X Tracker   │──→│   X Signals      │──→│  Decision    │
│               │   │                  │   │  Engine      │
│ - Ingesta     │   │ - NLP Analysis   │   │              │
│ - Métricas    │   │ - Clustering     │   │ - Strategies │
│               │   │ - Trending       │   │ - Risk Mgmt  │
└───────────────┘   └──────────────────┘   └──────┬───────┘
                                                   │
                                                   ↓
                                          ┌────────────────┐
                                          │    Trading     │
                                          │                │
                                          │ - Uniswap      │
                                          │ - Execution    │
                                          │ - Portfolio    │
                                          └────────────────┘
```

## 🎯 Componentes

### 1. Trading (`apps/trading`)
- **Responsabilidad**: Ejecución de operaciones en blockchain
- **Modelos**: `Wallet`, `Token`, `Position`, `Order`, `TransactionLog`
- **Servicios**:
  - `uniswap_client.py` - Cliente Web3 para Uniswap
  - `execution.py` - Lógica de ejecución de órdenes
  - `portfolio.py` - Gestión de posiciones y PnL

### 2. X Tracker (`apps/x_tracker`)
- **Responsabilidad**: Monitoreo de cuentas de X/Twitter
- **Modelos**: `TrackedAccount`, `Tweet`, `AccountMetrics`
- **Servicios**:
  - `x_client.py` - Wrapper API de Twitter
  - `ingestion.py` - Pipeline de ingesta de datos

### 3. X Signals (`apps/x_signals`)
- **Responsabilidad**: Análisis y extracción de señales
- **Modelos**: `TweetFeatures`, `SignalCluster`, `TrendingTopic`
- **Servicios**:
  - `preprocessing.py` - Limpieza y normalización
  - `feature_store.py` - Extracción de features
  - `similarity.py` - Clustering y comparación

### 4. Decision Engine (`apps/decision_engine`)
- **Responsabilidad**: Toma de decisiones de trading
- **Modelos**: `Strategy`, `TradingSignal`, `Decision`, `RiskMetrics`
- **Servicios**:
  - `strategies/` - Implementaciones de estrategias
  - `orchestrator.py` - Coordinación de señales
  - `risk.py` - Gestión de riesgo

## 🛠️ Stack Tecnológico

- **Framework**: Django 5.0
- **Database**: PostgreSQL
- **Cache/Queue**: Redis + Celery
- **Blockchain**: Web3.py + Uniswap Python
- **NLP**: Transformers (HuggingFace) + OpenAI
- **API**: Django REST Framework
- **Package Manager**: uv

## 📦 Instalación

### Pre-requisitos
- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- uv (gestor de paquetes)

### Setup

```bash
# 1. Instalar dependencias con uv
uv pip install -e .
uv pip install -e ".[dev]"

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 3. Ejecutar migraciones
cd src
python manage.py migrate

# 4. Crear superusuario
python manage.py createsuperuser

# 5. Cargar datos iniciales (opcional)
python manage.py loaddata initial_tokens
```

## 🚀 Ejecución

### Desarrollo

```bash
# Terminal 1: Django server
cd src
python manage.py runserver

# Terminal 2: Celery worker
cd src
celery -A infra.celery worker -l info

# Terminal 3: Celery beat (tareas programadas)
cd src
celery -A infra.celery beat -l info
```

### Producción

```bash
# Con Gunicorn + Supervisor/Systemd
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Celery workers
celery -A infra.celery worker -l info --concurrency=4

# Celery beat
celery -A infra.celery beat -l info
```

## 🔧 Configuración

### Variables de Entorno Clave

Ver `.env.example` para todas las variables disponibles.

**Esenciales**:
- `SECRET_KEY` - Clave secreta de Django
- `DB_*` - Credenciales de PostgreSQL
- `WEB3_PROVIDER_URI` - Endpoint RPC (Infura, Alchemy, etc.)
- `WALLET_PRIVATE_KEY` - Clave privada de la wallet de trading
- `X_*` - Credenciales de API de Twitter
- `OPENAI_API_KEY` - API key de OpenAI

## 📊 API Endpoints

### Health Check
```bash
GET /api/health/
```

### Trading
```bash
GET /api/positions/         # Todas las posiciones
GET /api/positions/open/    # Posiciones abiertas
GET /api/positions/closed/  # Posiciones cerradas
GET /api/orders/            # Todas las órdenes
GET /api/orders/pending/    # Órdenes pendientes
GET /api/orders/filled/     # Órdenes ejecutadas
```

### Signals & Decisions
```bash
GET /api/signals/           # Todas las señales
GET /api/signals/recent/    # Señales recientes
GET /api/decisions/         # Todas las decisiones
GET /api/decisions/approved/    # Decisiones aprobadas
GET /api/decisions/rejected/    # Decisiones rechazadas
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests por tipo
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/

# Con coverage
pytest --cov=apps --cov-report=html
```

## 📈 Flujo de Operación

1. **Ingesta**: Celery Beat ejecuta `fetch_all_tracked_accounts` cada 15 min
2. **Análisis**: Tweets → Features → Clustering → Trending Topics
3. **Señales**: Estrategias generan `TradingSignal` basadas en análisis
4. **Decisión**: Motor evalúa señales + riesgo → `Decision`
5. **Ejecución**: Decisiones aprobadas → `Order` → Blockchain
6. **Monitoreo**: Actualización de posiciones y métricas de riesgo

## 🔐 Seguridad

- **NUNCA** commitear `.env` con claves reales
- Usar hardware wallet o multisig para producción
- Implementar rate limiting en API
- Validar todas las transacciones antes de firmar
- Monitorear slippage y gas fees

## 📝 Tareas Pendientes de Implementación

- [ ] Implementar servicios de trading (uniswap_client, execution, portfolio)
- [ ] Implementar cliente de X/Twitter
- [ ] Implementar análisis NLP y sentiment
- [ ] Implementar estrategias de trading concretas
- [ ] Configurar monitoring con Prometheus + Grafana
- [ ] Implementar alertas (Telegram, Email)
- [ ] Backtest framework
- [ ] Paper trading mode

## 📄 Licencia

[Definir licencia]

## 👥 Contribución

[Definir guías de contribución]
