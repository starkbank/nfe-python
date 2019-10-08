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
                                <CNPJ>{senderTaxId}</CNPJ>
                            </CPFCNPJRemetente>
                        </Cabecalho>
                        <RPS>
                            <Assinatura>{rpsSignature}</Assinatura>
                            <ChaveRPS>
                                <InscricaoPrestador>{inscricaoPrestador}</InscricaoPrestador>
                                <SerieRPS>{serieRps}</SerieRPS>
                                <NumeroRPS>{numeroRps}</NumeroRPS>
                            </ChaveRPS>
                            <TipoRPS>{tipoRps}</TipoRPS>
                            <DataEmissao>{dataEmissao}</DataEmissao>
                            <StatusRPS>{statusRps}</StatusRPS>
                            <TributacaoRPS>{tributacaoRps}</TributacaoRPS>
                            <ValorServicos>{valorServicos}</ValorServicos>
                            <ValorDeducoes>{valorDeducoes}</ValorDeducoes>
                            <ValorPIS>{valorPis}</ValorPIS>
                            <ValorCOFINS>{valorCofins}</ValorCOFINS>
                            <ValorINSS>{valorInss}</ValorINSS>
                            <ValorIR>{valorIr}</ValorIR>
                            <ValorCSLL>{valorCsll}</ValorCSLL>
                            <CodigoServico>{codigoServico}</CodigoServico>
                            <AliquotaServicos>{aliquotaServicos}</AliquotaServicos>
                            <ISSRetido>{issRetido}</ISSRetido>
                            <CPFCNPJTomador>
                                <CNPJ>{receiverTaxId}</CNPJ>
                            </CPFCNPJTomador>
                            <RazaoSocialTomador>{receiverName}</RazaoSocialTomador>
                            <EnderecoTomador>
                                <Logradouro>{receiverStreetLine1}</Logradouro>
                                <NumeroEndereco>{receiverStreetNumber}</NumeroEndereco>
                                <ComplementoEndereco>{receiverStreetLine2}</ComplementoEndereco>
                                <Bairro>{receiverDistrict}</Bairro>
                                <Cidade>{receiverCity}</Cidade>
                                <UF>{receiverState}</UF>
                                <CEP>{receiverZipCode}</CEP>
                            </EnderecoTomador>
                            <EmailTomador>{receiverEmail}</EmailTomador>
                            <Discriminacao>{description}</Discriminacao>
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
                                    <DigestValue>{digestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{signatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{certificate}</X509Certificate>
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
                                <CNPJ>{senderTaxId}</CNPJ>
                            </CPFCNPJRemetente>
                            <transacao>true</transacao>
                        </Cabecalho>
                        <Detalhe>
                            <ChaveNFe>
                                <InscricaoPrestador>{inscricaoPrestador}</InscricaoPrestador>
                                <NumeroNFe>{nfeNumber}</NumeroNFe>
                            </ChaveNFe>
                            <AssinaturaCancelamento>{cancelSignature}</AssinaturaCancelamento>
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
                                    <DigestValue>{digestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{signatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{certificate}</X509Certificate>
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
                                <CNPJ>{senderTaxId}</CNPJ>
                            </CPFCNPJRemetente>
                            <CPFCNPJ>
                                <CNPJ>{senderTaxId}</CNPJ>
                            </CPFCNPJ>
                            <Inscricao>{inscricaoPrestador}</Inscricao>
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
                                    <DigestValue>{digestValue}</DigestValue>
                                </Reference>
                            </SignedInfo>
                            <SignatureValue>{signatureValue}</SignatureValue>
                            <KeyInfo>
                                <X509Data>
                                    <X509Certificate>{certificate}</X509Certificate>
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
