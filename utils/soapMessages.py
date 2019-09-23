# -*- coding: utf-8 -*-

# Schemas dos servicos para fazer a assinatura
# Toda vez que é gerado um novo envelope SOAP,
# deve conter um DigestValue diferente pois a assinatura
# do xml é feita na raiz da tag <MensagemXML> para a prefeitura de São Paulo.
# onde <MensagemXML> deve conter <![CDATA[ *MENSAGEM* ]]>
consultaCNPJ = """
<p1:PedidoConsultaCNPJ xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente></Cabecalho><CNPJContribuinte><CNPJ></CNPJ></CNPJContribuinte></p1:PedidoConsultaCNPJ>
"""

consultaNfePeriodo = """
<p1:PedidoConsultaNFePeriodo xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente><CPFCNPJ><CNPJ></CNPJ></CPFCNPJ><Inscricao></Inscricao><dtInicio>2019-06-01</dtInicio><dtFim>2019-07-01</dtFim><NumeroPagina>1</NumeroPagina></Cabecalho></p1:PedidoConsultaNFePeriodo>
"""

consultaNFe = """
<p1:PedidoConsultaNFe xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente></Cabecalho><Detalhe><ChaveNFe><InscricaoPrestador>57038597</InscricaoPrestador><NumeroNFe></NumeroNFe></ChaveNFe></Detalhe></p1:PedidoConsultaNFe>
"""

# Prazo de cancelamento da NFS-e: 20 dias
cancelamentoNota = """
<p1:PedidoCancelamentoNFe xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente><transacao>true</transacao></Cabecalho><Detalhe><ChaveNFe><InscricaoPrestador></InscricaoPrestador><NumeroNFe></NumeroNFe></ChaveNFe></Detalhe></p1:PedidoCancelamentoNFe>"""

# A assinatura do RPS deve ser feita em RSA-SHA1 antes de assinar a MensagemXML.
envioRPS = """
<p1:PedidoEnvioRPS xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente></Cabecalho><RPS><Assinatura></Assinatura><ChaveRPS><InscricaoPrestador></InscricaoPrestador><SerieRPS>OL03</SerieRPS><NumeroRPS>4105</NumeroRPS></ChaveRPS><TipoRPS>RPS-M</TipoRPS><DataEmissao>2019-07-01</DataEmissao><StatusRPS>N</StatusRPS><TributacaoRPS>T</TributacaoRPS><ValorServicos>11100</ValorServicos><ValorDeducoes>0</ValorDeducoes><ValorPIS>10</ValorPIS><ValorCOFINS>10</ValorCOFINS><ValorINSS>10</ValorINSS><ValorIR>10</ValorIR><ValorCSLL>10</ValorCSLL><CodigoServico></CodigoServico><AliquotaServicos></AliquotaServicos><ISSRetido></ISSRetido><CPFCNPJTomador><CNPJ></CNPJ></CPFCNPJTomador><RazaoSocialTomador></RazaoSocialTomador><EnderecoTomador><Logradouro></Logradouro><NumeroEndereco></NumeroEndereco><ComplementoEndereco></ComplementoEndereco><Bairro></Bairro><Cidade>3550308</Cidade><UF>SP</UF><CEP></CEP></EnderecoTomador><EmailTomador></EmailTomador><Discriminacao>Envio NFSe teste</Discriminacao></RPS></p1:PedidoEnvioRPS>"""


envioLoteRPS = """
<p1:PedidoEnvioLoteRPS xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Cabecalho Versao="1"><CPFCNPJRemetente><CNPJ></CNPJ></CPFCNPJRemetente><transacao>false</transacao><initDate>2019-07-01</initDate><endDate>2019-07-01</endDate><QtdRPS>1</QtdRPS><ValorTotalServicos>2</ValorTotalServicos><ValorTotalDeducoes>0</ValorTotalDeducoes></Cabecalho><RPS><Assinatura></Assinatura><ChaveRPS><InscricaoPrestador></InscricaoPrestador><SerieRPS>L003</SerieRPS><NumeroRPS>33</NumeroRPS></ChaveRPS><TipoRPS>RPS</TipoRPS><DataEmissao>2019-07-01</DataEmissao><StatusRPS>N</StatusRPS><TributacaoRPS>T</TributacaoRPS><ValorServicos>2</ValorServicos><ValorDeducoes>0</ValorDeducoes><CodigoServico>05895</CodigoServico><AliquotaServicos>0.029</AliquotaServicos><ISSRetido>false</ISSRetido><CPFCNPJTomador><CNPJ></CNPJ></CPFCNPJTomador><RazaoSocialTomador></RazaoSocialTomador><EnderecoTomador><Logradouro>Rua dos Ingleses</Logradouro><NumeroEndereco>586</NumeroEndereco><ComplementoEndereco>Apto 63</ComplementoEndereco><Bairro>Jardim Paulista</Bairro><Cidade>3550308</Cidade><UF>SP</UF><CEP>01329000</CEP></EnderecoTomador><EmailTomador>email@company.com.br</EmailTomador><Discriminacao>Envio NFSe teste</Discriminacao></RPS></p1:PedidoEnvioLoteRPS>"""
