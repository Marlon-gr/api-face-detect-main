@Library(['aic-jenkins-sharedlib']) _

pythonBuildPipeline {

    // Use virgulas para enviar para mais de um canal ao mesmo tempo:
    // canalRocketChat = 'abc,xyz,meu_canal_prioritario'
    // Use um ID do RocketChat para enviar para usuarios:
    // canalRocketChat = 'abc,@f1234567.nome.sobrenome,def'

    canaisNotificacao = ''

    habilitarValidacaoPreReq        = true
    habilitarValidacaoEstatica      = false
    habilitarValidacaoSeguranca     = true
    habilitarConstrucao             = true
    habilitarTestesUnidade          = false
    habilitarTestesIntegracao       = false
    habilitarTestesFumaca           = true
    habilitarSonar                  = false
    habilitarEmpacotamento          = true
    habilitarEmpacotamentoDocker    = true
    habilitarPublicacao             = true
    habilitarDebug                  = false
}
