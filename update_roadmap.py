#!/usr/bin/env python3
import re
import sys

roadmap_file = "ROADMAP.md"

try:
    with open(roadmap_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Erro: Arquivo {roadmap_file} não encontrado.", file=sys.stderr)
    sys.exit(1)

# Remove emojis de status dos títulos das seções para facilitar a identificação
cleaned_lines = []
for line in lines:
    cleaned_line = re.sub(r'(^## Fase [0-9]+(\.[0-9]+)?:.*)([ 	]*[📝✅🎯🔭]+)$', r'', line)
    cleaned_line = cleaned_line.rstrip()
    cleaned_lines.append(cleaned_line + '\n')
lines = cleaned_lines

fase1_content = []
fase1_5_content = []
fase2_content = []
fase3_old_content = []
fase4_old_content = []
other_content = []

current_section = "other"
for line_num, line in enumerate(lines):
    stripped_line = line.strip()
    if stripped_line == "## Fase 1: Fundação e MVP": # Adjusted to include 
        current_section = "fase1"
    elif stripped_line == "## Fase 1.5: Implementação do Sistema Jules-Flow": # Adjusted
        current_section = "fase1.5"
    elif stripped_line == "## Fase 2: Infraestrutura de Microserviços": # Adjusted
        current_section = "fase2"
    elif stripped_line == "## Fase 3: Módulo Piloto e Integração": # Adjusted
        current_section = "fase3_old"
    elif stripped_line == "## Fase 4: Governança e Maturidade": # Adjusted
        current_section = "fase4_old"
    elif stripped_line.startswith("## Fase") and current_section not in ["fase1", "fase1.5", "fase2", "fase3_old", "fase4_old"]:
        current_section = "other_unexpected" # This logic branch doesn't seem to be used later for content assignment

    if current_section == "fase1":
        fase1_content.append(line)
    elif current_section == "fase1.5":
        fase1_5_content.append(line)
    elif current_section == "fase2":
        fase2_content.append(line)
    elif current_section == "fase3_old":
        fase3_old_content.append(line)
    elif current_section == "fase4_old":
        fase4_old_content.append(line)
    elif current_section == "other": # Content before any recognized phase
        other_content.append(line)

if fase1_content: fase1_content.pop(0)
if fase1_5_content: fase1_5_content.pop(0)
if fase2_content: fase2_content.pop(0)
if fase3_old_content: fase3_old_content.pop(0)
if fase4_old_content: fase4_old_content.pop(0)

new_fase3_title = "## Fase 3: Melhorias do Frontend Core 📝\n"
new_fase3_content_text = (
    "\n"
    "**Épico:** Aprimorar a usabilidade, consistência e performance da interface principal da aplicação.\n"
    "*Objetivo: Refinar a experiência do usuário no 'core' da aplicação, estabelecendo uma base sólida para todos os módulos.*\n"
    "\n"
    "#### Tarefas Sugeridas:\n"
    "\n"
    "1.  **Implementar Notificações Globais (Toasts/Snackbars) no Core:** Implementar um mecanismo de notificação global (toasts/snackbars) no layout principal para dar feedback claro ao usuário sobre ações, erros ou informações importantes em pt-BR. Este sistema deverá ser utilizável por qualquer módulo.\n"
    "2.  **Revisão da Responsividade e Layout do Core:** Realizar uma auditoria e otimizar o layout do `MainLayout` e componentes centrais (como navegação, cabeçalho, rodapé, se houver) para garantir uma experiência de usuário consistente e agradável em dispositivos móveis e tablets. Manter o idioma pt-BR.\n"
    "3.  **Padronização de Componentes Visuais do Core:** Revisar os componentes visuais utilizados na interface principal (core) e criar/documentar um guia de estilo ou componentes reutilizáveis (ex: botões padrão, modais, cards) para garantir consistência visual. Todo o conteúdo em pt-BR.\n"
    "4.  **Melhoria na Navegação Principal e Feedback Visual do Core:** Avaliar a usabilidade da navegação principal (menu lateral, cabeçalho) e implementar melhorias no feedback visual de interações (ex: estados de hover, active, focus) para tornar a experiência mais intuitiva. Manter o idioma pt-BR.\n"
    "5.  **Otimização de Performance do Carregamento Inicial (Core):** Analisar e otimizar o tempo de carregamento inicial da aplicação principal, investigando o tamanho dos bundles, a estratégia de code splitting para o core e o carregamento de assets essenciais.\n"
)

new_fase4_title = "## Fase 4: Módulo Piloto e Integração 📝\n" # Emoji was 🎯, now 📝
new_fase5_title = "## Fase 5: Governança e Maturidade 🔭\n"

with open(roadmap_file, 'w', encoding='utf-8') as f:
    f.writelines(other_content)
    f.write("## Fase 1: Fundação e MVP ✅\n")
    f.writelines(fase1_content)
    f.write("---\n\n")
    f.write("## Fase 1.5: Implementação do Sistema Jules-Flow ✅\n")
    f.writelines(fase1_5_content)
    f.write("---\n\n")
    f.write("## Fase 2: Infraestrutura de Microserviços 🎯\n")
    f.writelines(fase2_content)
    f.write("---\n\n")
    f.write(new_fase3_title)
    f.write(new_fase3_content_text + "\n")
    f.write("---\n\n")
    f.write(new_fase4_title)
    f.writelines(fase3_old_content)
    f.write("---\n\n")
    f.write(new_fase5_title)
    f.writelines(fase4_old_content)

print(f"{roadmap_file} atualizado com sucesso usando Python.")
print("Verificando o conteúdo do ROADMAP.md atualizado:")
# with open(roadmap_file, 'r', encoding='utf-8') as f:
#     print(f.read())
