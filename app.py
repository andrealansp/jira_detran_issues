"""
Autor: André Alan Alves

Colossenses 3:2-5
Pensai nas coisas lá do alto, não nas que são aqui da terra; porque morrestes,
e a vossa vida está oculta juntamente com Cristo, em Deus.
Quando Cristo, que é a nossa vida, se manifestar, então,
vós também sereis manifestados com ele, em glória. Fazei,
pois, morrer a vossa natureza terrena: prostituição,
impureza, paixão lasciva, desejo maligno e a avareza, que é idolatria



Projeto realizado para integrar JIRA + SHAREPOINT + POWER APPS
"""

from typing import List

import shareplum
from shareplum.site import Version
import traceback

import config
from classes.funcoes import  Funcoes
from classes.acesso_jira import AcessoJira


# Carregar Lista do SharePoint, após essa carga utilizo a lista para verificar quais chamados da lista do sharepoint
# não está na lista do JIRA.
try:
    authcookie = shareplum.Office365(config.SHAREPOINT, username=config.USUARIO_365, password=config.SENHA).GetCookies()
    site = shareplum.Site(config.SHAREPOINT_SITE, version=Version.v2016, authcookie=authcookie)
    lista_chamados_abertos = site.List("chamados_abertos")
    chamados_abertos_sharepoint: List = lista_chamados_abertos.get_list_items('All Items')
except Exception as e:
    print(traceback.format_exc())
    print("Favor verificar usuário e senha ! - " + e.args[1])
    exit()

# Carregar chamados do JIRA, após esse carga do Jira utilizo a classe Funções para verificar quais chamados do jira
# Não está na lista do sharepoint.
chamados_abertos_jira: List = AcessoJira.pesquisar(config.JQL)

# rotina para verificar a diferença entre as listas do sharepoint e jira .
func = Funcoes()
diferenca_chamados_jira = func.retorna_chamados_diferentes(chamados_abertos_jira, chamados_abertos_sharepoint)
diferenca_chamados_sp = func.retorna_chamados_diferentes(chamados_abertos_sharepoint, chamados_abertos_jira)

# Quando há a diferença no jira, criamos os chamados.
if diferenca_chamados_jira:
    lista_chamados_abertos.UpdateListItems(data=diferenca_chamados_jira, kind='New')
else:
    print("Sem chamados para adicionar")

# Excluir Chamados do jira já resolvidos na lista do sharepoint.
if diferenca_chamados_sp:
    lista_ids_delete: List = []
    for chamado_a_excluir in diferenca_chamados_sp:
        lista_ids_delete.append(chamado_a_excluir['ID'])
    lista_chamados_abertos.update_list_items(data=lista_ids_delete, kind="Delete")
else:
    print("Sem chamados para excluir")

# Carrega o novo status da Lista do share point, compara com a lista do Jira e atualiza
share_point_atualizada = site.List("chamados_abertos")
lista_atualizada_sharepoint = share_point_atualizada.GetListItems("All Items")

atualizacao_chamados: List = func.verifica_status_chamado(lista_atualizada_sharepoint, chamados_abertos_jira)

share_point_atualizada.UpdateListItems(data=atualizacao_chamados, kind='Update')



