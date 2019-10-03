from re import search, compile, IGNORECASE, sub

from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from xmlsigner.Integer import b64e

# certificateFile = "../utils/converted.crt"
privateKeyRSA = "../utils/RSAPrivateKey.pem"

# privateKeyContent = open(privateKeyRSA).read()
# certificateContent = open(certificateFile).read()
rsaKeyContent = open(privateKeyRSA).read()

xml = """
<?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
    <soap12:Body>
        <EnvioRPSRequest xmlns="http://www.prefeitura.sp.gov.br/nfe">
            <VersaoSchema>1</VersaoSchema>
                <MensagemXML>
                    <![CDATA[
                    <p1:PedidoEnvioRPS xmlns:p1="http://www.prefeitura.sp.gov.br/nfe" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <Cabecalho xmlns="" Versao="1">
                            <CPFCNPJRemetente><CNPJ>{senderTaxId}</CNPJ></CPFCNPJRemetente>
                        </Cabecalho>
                        <RPS xmlns="">
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
                            <ValorIR>{valorIR}</ValorIR>
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
                                <NumeroEndereco>receiverStreetNumber</NumeroEndereco>
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
                            <SignedInfo><CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                            <SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                            <Reference URI=""><Transforms><Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/><Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                            </Transforms>
                                <DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                                <DigestValue>/bdJplrF7P6EMypWHbWIvHo//k8=</DigestValue></Reference>
                            </SignedInfo>
                                <SignatureValue>tc4jXC3HGP1RFmu0XRUMi06FJ5UlV6OYCFE+yBuAOqAiIQFpQv9fx5FFlE2ti5NQd0WdYbnQH6of3DHmt66ZpJsFrqx/SYOP3IzW8WNXmttYNrqomlPbK8B4WiWk3q+sIllarrCYd0YugFaHLfT9O3B7pE4W4SgdKF1ZjnfRVklF6oxhr5iq12GApGY+KixXDwlL3lys4BwLwZYGIuE+jzsQmuiJNIUpWuuuxvg1zNRUO8WBoDlHQjOeUaA1RiC/amYb1uOZ8eBzBP+8UNe3ZpGEkNadXakhh4vhJi685UrZo3FIXP1GDSPfkqfsO8JAxY9thfgeXGZykFjH/Cefhw==</SignatureValue>
                                <KeyInfo>
                                    <X509Data><X509Certificate>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</X509Certificate></X509Data>
                                </KeyInfo>
                        </Signature>
                    </p1:PedidoEnvioRPS>
                    ]]>
                </MensagemXML>
            </EnvioRPSRequest>
    </soap12:Body>
</soap12:Envelope>
"""


def sign(text):
    digest = SHA.new(text)
    rsaKey = RSA.importKey(rsaKeyContent)
    signer = PKCS1_v1_5.new(rsaKey)
    sign = signer.sign(digest)
    return b64e(sign)


def nota(xml, inscricaoPrestador, serieRps, numeroRps, dataEmissao, statusRps, valorServicos,
         valorDeducoes, codigoServico, issRetido, receiverTaxId, senderTaxId):

    rpsToSign = "{inscricaoPrestador}{serieRps}{numeroRps}{dataEmissao}{statusRps}" \
                "{issRetido}{valorServicos}{valorDeducoes}{codigoServico}2{receiverTaxId}".format(
        inscricaoPrestador=inscricaoPrestador.zfill(8),
        serieRps=serieRps.ljust(5).upper(),
        numeroRps=numeroRps.zfill(12),
        dataEmissao=dataEmissao.replace("-", ""),
        statusRps=statusRps,
        issRetido=issRetido,
        valorServicos=str(valorServicos).zfill(15),
        valorDeducoes=str(valorDeducoes).zfill(15),
        codigoServico=codigoServico.zfill(5),
        receiverTaxId=receiverTaxId.zfill(14),
    )

    bodyToSign = search("<!\[CDATA\[(.*\n*\s*)*\]\]>", xml).group(1)

    bodySignature = sign(bodyToSign)
    rpsSignature = sign(rpsToSign)

    # envelope = xml.format(
    #     senderTaxId=senderTaxId,
    #     rpsSignature=b64Signed
    # )


    #<!\[CDATA\[(\s*.*)*<

nota(
    xml=xml,
    inscricaoPrestador="",
    serieRps="",
    numeroRps="",
    dataEmissao="",
    statusRps="",
    valorServicos="",
    valorDeducoes="",
    codigoServico="",
    issRetido="",
    receiverTaxId="30134945000167",
    senderTaxId="20018183000180"
)




