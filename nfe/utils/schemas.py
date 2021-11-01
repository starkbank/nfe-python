schemaCreateRps = """
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <EnvioRPSRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
            <VersaoSchema>1</VersaoSchema>
                <MensagemXML>
                    <![CDATA[
                    <p1:PedidoEnvioRPS xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Cabecalho Versao="1">
                            <CPFCNPJRemetente>
                                <CNPJ>{CPFCNPJRemetente}</CNPJ>
                            </CPFCNPJRemetente>
                        </Cabecalho>
                        <RPS>
                            <Assinatura>{Assinatura}</Assinatura>
                            <ChaveRPS>
                                <InscricaoPrestador>{InscricaoPrestador}</InscricaoPrestador>
                                <SerieRPS>{SerieRPS}</SerieRPS>
                                <NumeroRPS>{NumeroRPS}</NumeroRPS>
                            </ChaveRPS>
                            <TipoRPS>{TipoRPS}</TipoRPS>
                            <DataEmissao>{DataEmissao}</DataEmissao>
                            <StatusRPS>{StatusRPS}</StatusRPS>
                            <TributacaoRPS>{TributacaoRPS}</TributacaoRPS>
                            <ValorServicos>{ValorServicos}</ValorServicos>
                            <ValorDeducoes>{ValorDeducoes}</ValorDeducoes>
                            <ValorPIS>{ValorPIS}</ValorPIS>
                            <ValorCOFINS>{ValorCOFINS}</ValorCOFINS>
                            <ValorINSS>{ValorINSS}</ValorINSS>
                            <ValorIR>{ValorIR}</ValorIR>
                            <ValorCSLL>{ValorCSLL}</ValorCSLL>
                            <CodigoServico>{CodigoServico}</CodigoServico>
                            <AliquotaServicos>{AliquotaServicos}</AliquotaServicos>
                            <ISSRetido>{ISSRetido}</ISSRetido>
                            <CPFCNPJTomador>
                                <{CPFCNPJTomadorTag}>{CPFCNPJTomador}</{CPFCNPJTomadorTag}>
                            </CPFCNPJTomador>
                            <RazaoSocialTomador>{RazaoSocialTomador}</RazaoSocialTomador>
                            <EnderecoTomador>
                                <Logradouro>{Logradouro}</Logradouro>
                                <NumeroEndereco>{NumeroEndereco}</NumeroEndereco>
                                <ComplementoEndereco>{ComplementoEndereco}</ComplementoEndereco>
                                <Bairro>{Bairro}</Bairro>
                                <Cidade>{Cidade}</Cidade>
                                <UF>{UF}</UF>
                                <CEP>{CEP}</CEP>
                            </EnderecoTomador>
                            <EmailTomador>{EmailTomador}</EmailTomador>
                            <Discriminacao>{Discriminacao}</Discriminacao>
                        </RPS>
                        <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
                            <SignedInfo>
                                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod>
                                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod>
                                <Reference URI="">
                                    <Transforms>
                                        <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform>
                                        <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></Transform>
                                    </Transforms>
                                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>
                                    <DigestValue>{DigestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{SignatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{X509Certificate}</X509Certificate>
                                </X509Data>
                            </KeyInfo>
                        </Signature>
                    </p1:PedidoEnvioRPS>
                    ]]>
                </MensagemXML>
            </EnvioRPSRequest>
    </soap12:Body>
</soap12:Envelope>
"""


schemaCancelRps = """
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <CancelamentoNFeRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
            <VersaoSchema>1</VersaoSchema>
                <MensagemXML>
                    <![CDATA[
                    <p1:PedidoCancelamentoNFe xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Cabecalho Versao="1">
                            <CPFCNPJRemetente>
                                <CNPJ>{CPFCNPJRemetente}</CNPJ>
                            </CPFCNPJRemetente>
                            <transacao>true</transacao>
                        </Cabecalho>
                        <Detalhe>
                            <ChaveNFe>
                                <InscricaoPrestador>{InscricaoPrestador}</InscricaoPrestador>
                                <NumeroNFe>{NumeroNFe}</NumeroNFe>
                            </ChaveNFe>
                            <AssinaturaCancelamento>{AssinaturaCancelamento}</AssinaturaCancelamento>
                        </Detalhe>
                        <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
                            <SignedInfo>
                                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod>
                                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod>
                                <Reference URI="">
                                    <Transforms>
                                        <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform>
                                        <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></Transform>
                                    </Transforms>
                                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>
                                    <DigestValue>{DigestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{SignatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{X509Certificate}</X509Certificate>
                                </X509Data>
                            </KeyInfo>
                        </Signature>
                    </p1:PedidoCancelamentoNFe>
                    ]]>
                </MensagemXML>
            </CancelamentoNFeRequest>
    </soap12:Body>
</soap12:Envelope>
"""

schemaConsultNfes = """
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <ConsultaNFeEmitidasRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
            <VersaoSchema>1</VersaoSchema>
                <MensagemXML>
                    <![CDATA[
                    <p1:PedidoConsultaNFePeriodo xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Cabecalho Versao="1">
                            <CPFCNPJRemetente>
                                <CNPJ>{CPFCNPJRemetente}</CNPJ>
                            </CPFCNPJRemetente>
                            <CPFCNPJ>
                                <CNPJ>{CPFCNPJRemetente}</CNPJ>
                            </CPFCNPJ>
                            <Inscricao>{Inscricao}</Inscricao>
                            <dtInicio>{dtInicio}</dtInicio>
                            <dtFim>{dtFim}</dtFim>
                            <NumeroPagina>1</NumeroPagina>
                        </Cabecalho>
                        <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
                            <SignedInfo>
                                <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></CanonicalizationMethod>
                                <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"></SignatureMethod>
                                <Reference URI="">
                                    <Transforms>
                                        <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"></Transform>
                                        <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"></Transform>
                                    </Transforms>
                                    <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"></DigestMethod>
                                    <DigestValue>{DigestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{SignatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{X509Certificate}</X509Certificate>
                                </X509Data>
                            </KeyInfo>
                        </Signature>
                    </p1:PedidoConsultaNFePeriodo>
                    ]]>
                </MensagemXML>
            </ConsultaNFeEmitidasRequest>
    </soap12:Body>
</soap12:Envelope>
"""
