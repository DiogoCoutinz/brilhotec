# BrilhoTec — Website

Site institucional da BrilhoTec — pinturas, alpinismo industrial e reabilitação de edifícios.

Stack: HTML estático + CSS + JS (zero dependências). Pronto para Vercel.

## Estrutura

```
.
├── index.html              # one-page principal
├── assets/
│   ├── css/style.css       # design system BrilhoTec
│   ├── js/main.js          # nav mobile, scroll reveal
│   └── img/
│       ├── logo.svg
│       └── favicon.svg
├── sitemap.xml             # SEO
├── robots.txt              # SEO
├── vercel.json             # headers de segurança + cache
└── README.md
```

---

## Checklist antes de publicar

### 1. Substituições obrigatórias no `index.html`

| Placeholder | Substituir por |
|---|---|
| `+351 000 000 000` (e `tel:+351000000000`) | Telefone real da BrilhoTec |
| `geral@brilhotec.pt` | Email real (no schema JSON-LD também) |
| `wa.me/351000000000` | Nº WhatsApp real (sem `+` nem espaços) |
| `SUBSTITUIR_FORM_ID` | ID do formulário Formspree (ver passo 2) |
| `https://brilhotec.vercel.app/` | URL final assim que tiveres (canonical, OG, schema, sitemap, robots) |

### 2. Configurar o formulário de contacto (Formspree)

O formulário precisa de **guardar os pedidos**. Recomendo Formspree — gratuito até 50 envios/mês, dashboard com histórico, exporta CSV, recebes email a cada envio.

**Passos (5 minutos):**

1. Criar conta em [formspree.io](https://formspree.io) (gratuita)
2. **New Form** → escolher email para receber notificações (`geral@brilhotec.pt`)
3. Copiar o endpoint (formato: `https://formspree.io/f/xpzaxxxx`)
4. No [index.html](index.html), procurar `SUBSTITUIR_FORM_ID` e colar lá apenas o ID (`xpzaxxxx`)
5. Activar protecção anti-spam no painel Formspree (já vem com honeypot no HTML)

**Para ver os pedidos:** entrar no dashboard Formspree → Submissions. Cada pedido fica guardado lá + recebes email.

### 3. Fotos das obras (Galeria)

A secção **Trabalhos** tem 6 slots com placeholders (gradientes navy/dourado + ícones). Substituir por fotos reais:

- Tamanho recomendado: 800×600 ou 1200×900px, formato `.webp` ou `.jpg`
- Guardar em `assets/img/galeria/` (ex: `pintura-fachada.jpg`)
- No CSS [style.css](assets/css/style.css), procurar `.gi-1 .gallery-img` (e gi-2, gi-3...) e trocar o `background:` por `background-image: url('/assets/img/galeria/nome-da-foto.jpg')`

### 4. Logo

O `logo.svg` é uma aproximação fiel ao logo da `image.png`. Para produção, pedir ao designer o ficheiro vetorial original e substituir `assets/img/logo.svg` + `assets/img/favicon.svg`.

### 5. Imagem OG (partilhas em WhatsApp / Facebook / LinkedIn)

Colocar `og-image.jpg` em `assets/img/` (1200×630px). Ideal: foto de obra + logo BrilhoTec sobreposto.

---

## Correr localmente

```bash
python3 -m http.server 5173
# Abrir http://localhost:5173
```

Alternativas: `npx serve .`, `npx live-server`.

---

## Deploy no Vercel

### Opção A — CLI (mais rápido)

```bash
cd /Users/diogocoutinho/Projetos/Brilhotec
npx vercel              # primeiro deploy (preview)
npx vercel --prod       # publicar em produção
```

Na primeira execução pede login e config do projecto. Deixar tudo default — é site estático.

### Opção B — GitHub + Vercel

1. Criar repositório GitHub e fazer push
2. Em [vercel.com/new](https://vercel.com/new), importar o repo
3. Framework Preset: **Other**
4. Deploy

### Adicionar domínio próprio (quando comprares)

Painel Vercel → Settings → Domains → adicionar `brilhotec.pt` e `www.brilhotec.pt`. Configurar os DNS conforme indicado pela Vercel.

**Depois disso, voltar a editar:**
- `index.html` → substituir `https://brilhotec.vercel.app/` por `https://brilhotec.pt/` (4 ocorrências)
- `sitemap.xml` → mesmo
- `robots.txt` → mesmo

---

## SEO — o que está feito

- `<title>` e `<meta description>` optimizados em PT-PT
- Open Graph + Twitter Card
- Schema.org `LocalBusiness` + `Organization` (JSON-LD)
- Canonical URL
- `sitemap.xml` + `robots.txt`
- HTML semântico (header, main, section, footer, figure)
- Headings hierárquicos (h1 → h2 → h3)
- Mobile-first responsivo
- Sem frameworks (fast LCP), fontes via Google Fonts com `preconnect`
- Headers de segurança via `vercel.json` (HSTS, X-Frame-Options, etc.)
- Cache imutável de assets (1 ano)

---

## Próximos passos sugeridos

1. **Google Search Console** — submeter o `sitemap.xml` após deploy. URL: `https://search.google.com/search-console`
2. **Google Business Profile** — criar/optimizar para SEO local (aparecer no Maps quando alguém procura "pinturas em [cidade]")
3. **Analytics** — adicionar [Plausible](https://plausible.io) ou [Umami](https://umami.is) (preferíveis a GA4 por RGPD)
4. **Galeria com fotos reais** — fotos antes/depois aumentam muito a conversão
5. **Testemunhos de clientes** — secção dedicada com 3–5 reviews reais
6. **Páginas dedicadas por serviço** — para SEO long-tail (`/pintura-fachadas`, `/alpinismo-industrial`, etc.)
7. **Blog** — artigos tipo "Quando impermeabilizar o telhado?" trazem tráfego orgânico
