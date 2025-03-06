from __future__ import annotations

from typing import cast, List

import jirapt
from jira import JIRA
from jira.client import ResultList
from jira.resources import Issue
from datetime import datetime

import config


class AcessoJira:
    def __init__(self):
        pass

    @staticmethod
    def pesquisar(jql):
        """
        Retorna a lista de dicionários com chamados do jira
        :param jql:
        :return: lista_chamados
        """
        # Some Authentication Methods
        jira = JIRA(basic_auth=(config.USER_JIRA, config.API_TOKEN),
                    server=config.SERVIDOR)

        myself = jira.myself()

        issues = cast(ResultList[Issue], jirapt.search_issues(jira, jql, 2))

        lista_chamados: List = []
        for chamado in issues:
            if not chamado.fields.customfield_10063.ongoingCycle.breached:
                lista_chamados.append({
                    "CHAVE": chamado.key,
                    "RESUMO": chamado.fields.summary,
                    "PONTO": chamado.fields.customfield_10060.child.value,
                    "REQUEST TYPE": chamado.fields.customfield_10010.requestType.name,
                    "EQUIPAMENTO": f'{chamado.fields.customfield_10060.value} - {chamado.fields.customfield_10060.child.value}',
                    "DATA CRIAÇÃO": datetime.fromisoformat(chamado.fields.created[0:23]).strftime("%d/%m/%y - %H:%M"),
                    "DATA PARA VENCIMENTO": chamado.fields.customfield_10063.ongoingCycle.breachTime.friendly,
                    "VENCIDO": 'NO PRAZO'
                })
            else:
                lista_chamados.append({
                    "CHAVE": chamado.key,
                    "RESUMO": chamado.fields.summary,
                    "PONTO": chamado.fields.customfield_10060.child.value,
                    "REQUEST TYPE": chamado.fields.customfield_10010.requestType.name,
                    "EQUIPAMENTO": f'{chamado.fields.customfield_10060.value} - {chamado.fields.customfield_10060.child.value}',
                    "DATA CRIAÇÃO": datetime.fromisoformat(chamado.fields.created[0:23]).strftime("%d/%m/%y - %H:%M"),
                    "DATA PARA VENCIMENTO": chamado.fields.customfield_10063.ongoingCycle.breachTime.friendly,
                    "VENCIDO": "FORA DO PRAZO"
                })

        return lista_chamados
