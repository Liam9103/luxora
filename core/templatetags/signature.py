from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def dev_signature():
    html = """
    <style>
        @keyframes signatureGlow {
            0%, 100% { box-shadow: 0 5px 20px rgba(212, 175, 55, 0.15); }
            50% { box-shadow: 0 5px 30px rgba(212, 175, 55, 0.4); }
        }
        @keyframes sparkleRotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .dev-signature-badge {
            position: fixed;
            bottom: 24px;
            left: 24px;
            z-index: 9998;
            background: linear-gradient(135deg, rgba(10,10,15,0.9), rgba(20,20,31,0.9));
            backdrop-filter: blur(12px);
            border: 1px solid rgba(212, 175, 55, 0.35);
            padding: 10px 20px;
            border-radius: 50px;
            font-size: 0.76rem;
            color: rgba(255,255,255,0.7);
            font-family: 'Poppins', sans-serif;
            display: flex;
            align-items: center;
            gap: 8px;
            animation: signatureGlow 3s ease-in-out infinite;
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .dev-signature-badge:hover {
            transform: translateY(-6px) scale(1.03);
            border-color: #D4AF37;
            color: #fff;
        }
        .dev-signature-badge .spark {
            display: inline-block;
            color: #D4AF37;
            animation: sparkleRotate 4s linear infinite;
        }
        .dev-signature-badge strong {
            color: #D4AF37;
            font-weight: 700;
        }
        @media (max-width: 768px) {
            .dev-signature-badge { bottom: 16px; left: 16px; padding: 8px 16px; font-size: 0.68rem; }
        }
    </style>
    <div class="dev-signature-badge">
        <span class="spark">✦</span>
        <span>Crafted by <strong>Ilia Pirmarzabad</strong></span>
    </div>
    """
    return mark_safe(html)