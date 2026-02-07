def template_basic_business(name: str) -> dict:
    return {
        "theme": {"primary": "#111827", "font": "Inter"},
        "sections": [
            {
                "type": "Hero",
                "props": {
                    "title": name,
                    "subtitle": "Servicio profesional para tu negocio",
                    "ctaText": "Cotizar",
                },
            },
            {
                "type": "Features",
                "props": {
                    "items": [
                        {"title": "Rápido", "desc": "Atención inmediata"},
                        {"title": "Confiable", "desc": "Resultados garantizados"},
                        {"title": "Soporte", "desc": "Te acompañamos en todo"},
                    ]
                },
            },
            {
                "type": "CTA",
                "props": {"text": "¿Listo para empezar?", "button": "WhatsApp", "href": "https://wa.me/"},
            },
            {"type": "Footer", "props": {"text": f"© {name}"}},
        ],
    }

