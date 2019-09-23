from utils import soapMessages
from utils.formatCurrency import Currency
from xmlsigner.postXml import PostXML
from xmlsigner.signerXml import SignCert
from lxml import etree


class Services(object):

    def __init__(self, certificateContent, rsaKeyContent, privateKeyContent=None):
        self.objSignCert = SignCert(
            privateKeyContent=privateKeyContent,
            certificateContent=certificateContent,
            rsaKeyContent=rsaKeyContent
        )
        self.objSignCert.loadPem()
        self.postObj = PostXML(cert=certificateContent, key=rsaKeyContent)

    def consultTaxIdSubscription(self, taxId, taxPayerId):
        taxIdRequestTree = etree.fromstring(soapMessages.consultaCNPJ)
        taxIdRequestTree.find('.//CNPJ', namespaces={}).text = taxId
        taxIdRequestTree.find('.//CNPJContribuinte/CNPJ', namespaces={}).text = taxPayerId
        signedRequest = self.objSignCert.signWithA1Cert(taxIdRequestTree)
        return self.postObj.consultSubscription(signedXml=signedRequest)

    def consultNfe(self, nfe, taxId):
        nfeRequestTree = etree.fromstring(soapMessages.consultaNFe)
        nfeRequestTree.find('.//CNPJ', namespaces={}).text = taxId
        nfeRequestTree.find('.//NumeroNFe', namespaces={}).text = nfe
        signedRequest = self.objSignCert.signWithA1Cert(bufferXml=nfeRequestTree)
        return self.postObj.consultNfe(signedXml=signedRequest)

    def sendRPS(self, taxId, providerSubscription, rpsSeries, rpsNumber, rpsType, issueDate, rpsStatus, issRetain,
                rpsTax, servicesAmount, deductionsAmount, pisAmount, cofinsAmount, inssAmount, irAmount,
                csllAmount, serviceCode, aliquot, takerTaxId, companyName, streetLine, streetNumber,
                streetLine2, district, zipCode, email, description):
        sendRpsTree = etree.fromstring(soapMessages.envioRPS)
        sendRpsTree.find('.//CNPJ', namespaces={}).text = taxId
        sendRpsTree.find('.//InscricaoPrestador', namespaces={}).text = providerSubscription
        sendRpsTree.find('.//SerieRPS', namespaces={}).text = rpsSeries
        sendRpsTree.find('.//NumeroRPS', namespaces={}).text = rpsNumber
        sendRpsTree.find('.//TipoRPS', namespaces={}).text = rpsType
        sendRpsTree.find('.//DataEmissao', namespaces={}).text = issueDate
        sendRpsTree.find('.//StatusRPS', namespaces={}).text = rpsStatus
        sendRpsTree.find('.//TributacaoRPS', namespaces={}).text = rpsTax
        sendRpsTree.find('.//ValorServicos', namespaces={}).text = Currency.formatted(servicesAmount)
        sendRpsTree.find('.//ValorDeducoes', namespaces={}).text = Currency.formatted(deductionsAmount)
        sendRpsTree.find('.//ValorPIS', namespaces={}).text = Currency.formatted(pisAmount)
        sendRpsTree.find('.//ValorCOFINS', namespaces={}).text = Currency.formatted(cofinsAmount)
        sendRpsTree.find('.//ValorINSS', namespaces={}).text = Currency.formatted(inssAmount)
        sendRpsTree.find('.//ValorIR', namespaces={}).text = Currency.formatted(irAmount)
        sendRpsTree.find('.//ValorCSLL', namespaces={}).text = Currency.formatted(csllAmount)
        sendRpsTree.find('.//AliquotaServicos', namespaces={}).text = Currency.formatted(aliquot)
        sendRpsTree.find('.//CodigoServico', namespaces={}).text = serviceCode
        sendRpsTree.find('.//CPFCNPJTomador/CNPJ', namespaces={}).text = takerTaxId
        sendRpsTree.find('.//RazaoSocialTomador', namespaces={}).text = companyName
        sendRpsTree.find('.//EnderecoTomador/Logradouro', namespaces={}).text = streetLine.decode("utf-8")
        sendRpsTree.find('.//EnderecoTomador/NumeroEndereco', namespaces={}).text = streetNumber
        sendRpsTree.find('.//EnderecoTomador/ComplementoEndereco', namespaces={}).text = streetLine2.decode("utf-8")
        sendRpsTree.find('.//EnderecoTomador/Bairro', namespaces={}).text = district.decode("utf-8")
        sendRpsTree.find('.//EnderecoTomador/CEP', namespaces={}).text = zipCode
        sendRpsTree.find('.//EmailTomador', namespaces={}).text = email
        sendRpsTree.find('.//Discriminacao', namespaces={}).text = description.decode("utf-8") if description else None
        sendRpsTree.find('.//ISSRetido', namespaces={}).text = issRetain
        signedRPS = self.objSignCert.signRps(sendRpsTree)
        return self.postObj.sendRPS(signedXml=signedRPS)

    def bulkingRPS(self):
        signedEnvioLoteRPS = self.objSignCert.signLoteRps(soapMessages.envioLoteRPS)
        return self.postObj.bulkRPS(signedXml=signedEnvioLoteRPS)

    def cancelNfe(self, taxId, providerSubscription, nfeNum):
        cancelTree = etree.fromstring(soapMessages.cancelamentoNota)
        cancelTree.find('.//CNPJ', namespaces={}).text = taxId
        cancelTree.find('.//InscricaoPrestador', namespaces={}).text = providerSubscription
        cancelTree.find('.//NumeroNFe', namespaces={}).text = str(nfeNum)
        signedCancelContent = self.objSignCert.signCancel(cancelTree)
        return self.postObj.cancelNfe(signedXml=signedCancelContent)

    def consultReceivedNfe(self, taxId, initDate, endDate, receiverTaxId, subscription):
        consultTree = etree.fromstring(soapMessages.consultaNfePeriodo)
        consultTree.find('.//CPFCNPJRemetente/CNPJ', namespaces={}).text = taxId
        consultTree.find('.//dtInicio', namespaces={}).text = initDate
        consultTree.find('.//dtFim', namespaces={}).text = endDate
        consultTree.find('.//CPFCNPJ/CNPJ', namespaces={}).text = receiverTaxId
        consultTree.find('.//Inscricao', namespaces={}).text = subscription
        signedReceivedTree = self.objSignCert.signWithA1Cert(consultTree)
        return self.postObj.consultReceivedNfe(signedXml=signedReceivedTree)

    def consultSentNfe(self, taxId, initDate, endDate, providerTaxId, subscription):
        consultTree = etree.fromstring(soapMessages.consultaNfePeriodo)
        consultTree.find('.//CPFCNPJRemetente/CNPJ', namespaces={}).text = taxId
        consultTree.find('.//dtInicio', namespaces={}).text = initDate
        consultTree.find('.//dtFim', namespaces={}).text = endDate
        consultTree.find('.//CPFCNPJ/CNPJ', namespaces={}).text = providerTaxId
        consultTree.find('.//Inscricao', namespaces={}).text = subscription
        signedSentTree = self.objSignCert.signWithA1Cert(consultTree)
        return self.postObj.consultSentNfe(signedXml=signedSentTree)
