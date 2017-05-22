# Especificação dos Casos de Uso

## Cadastrar no Sistema

### Resumo

O ator Usuário realiza o seu cadastro no sistema.

### Atores

* Usuário

### Pós-condições

* O ator Usuário é cadastrado com sucesso no sistema.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário abre a *landing page*.

2. O ator Usuário seleciona a opção de realizar cadastro.

3. O ator Usuário insere o código do Módulo.

4. O ator Usuário insere suas informações no formulário de cadastro.

5. O ator Usuário submete o formulário para a finalização do processo.

#### Fluxos Alternativos

##### 3a: O código do Módulo é inválido

1. O sistema informa ao usuário que o código informado é inválido e impossibilita a continuação do cadastro.

##### 4a: O ator já está cadastrado

1. O sistema já informa que o email informado no formulário já está cadastrado.

## Autenticar

### Resumo

O ator Usuário, Dependente ou Administrador autentica-se no sistema.

### Atores

* Usuário

* Dependente

* Administrador

### Precondições

* O ator (Usuário, Dependente ou Administrador) é cadastrado no sistema.

### Fluxos de Evento

#### Fluxo Básico

1. O ator abre a *landing page*.

2. O ator decide realizar *login*.

3. O ator Usuário insere suas informações no formulário de autenticação.

4. O ator Usuário submete o formulário para a finalização do processo.

#### Fluxos Alternativos

##### 2a: O ator esqueceu a senha

1. O ator informa que esqueceu a senha.

2. O sistema solicita o email cadastrado.

3. O ator informa o email.

4. O sistema envia um email de redefinição de senha para o email informado.

## Gerenciar Perfil

### Resumo

O usuário pode editar suas informações pessoais e salvando-as no sistema.

### Atores

* Usuário

### Precondições

* O ator Usuário deve estar autenticado.

### Pós-condições

* As informações são atualizadas e propagadas para as sessões ativas.

### Fluxos de Evento

#### Fluxo Básico

6. O ator Usuário abre a página do perfil.

7. O ator Usuário realiza as modificações.

8. O ator Usuário salva as modificações.

#### Fluxos Alternativos

##### 1a: O ator não está cadastrado

2. O ator Usuário realiza o cadastro das credenciais, antes de avançar.

## Gerenciar Usuários Dependentes

### Resumo

O usuário visualiza, adiciona ou remove usuários dependentes enviando uma solicitação de vínculo.

### Atores

* Usuário

### Precondições

* O ator Usuário deve estar autenticado.

### Pós-condições

* O sistema deve cadastrar o Usuário Dependente e notificá-lo.

### Fluxos de Evento

1. O ator Usuário acessa a seção de Usuários Dependentes.

2. O ator Usuário decide adicionar, editar ou excluir.

3. O ator Usuário acessa o formulário de Usuário Dependente.

4. O ator Usuário realiza as modificações.

5. O ator Usuário salva as modificações.

## Gerenciar Contatos de Emergência

### Resumo

O usuário visualiza, adiciona ou remove contatos de emergência que podem ser alertados automaticamente via email, mensagem no Facebook ou Twitter.

### Atores

* Usuário

### Precondições

* O ator Usuário deve estar autenticado no sistema.

### Pós-condições

* O sistema deve notificar os Contatos de Emergência se houve modificações.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário acessa a seção de Contatos de Emergência.

2. O ator Usuário decide adicionar, editar ou excluir.

3. O ator Usuário acessa o formulário de Contato de Emergência.

4. O ator Usuário realiza as modificações.

5. O ator Usuário salva as modificações.

## Gerenciar Módulos Adquiridos

### Resumo

O usuário ou dependente cadastra, altera ou remove seus módulos adquiridos.

### Atores

* Usuário

* Dependente

### Precondições

* O ator Usuário ou Dependente deve estar autenticado no sistema.

### Pós-condições

* O sistema deve validar, ativar e vincular o módulo ao Usuário.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário ou Dependente acessa a seção de Módulos.

2. O ator Usuário ou Dependente decide adicionar, editar ou excluir.

3. O ator Usuário ou Dependente acessa o formulário de Módulo.

4. O ator Usuário ou Dependente realiza as modificações.

5. O ator Usuário ou Dependente salva as modificações.

## Controlar Módulos Adquiridos

### Resumo

O usuário ou dependente pode controlar o estado dos módulos.

### Atores

* Usuário

* Dependente

* Broker

### Precondições

* O ator Usuário ou Dependente deve estar autenticado no sistema.

### Pós-condições

* O ator Broker deve retornar o estado do módulo, se houver modificações.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário ou Dependente acessa a seção de Módulos.

2. O ator Usuário ou Dependente decide realizar alguma alteração de estado em algum módulo.

3. O sistema envia a modificação para o ator Broker.

4. O ator Broker envia a modificação para o módulo.

## Acompanhar Módulos Adquiridos

### Resumo

O usuário ou dependente visualiza através de um painel o estado dos módulos.

### Atores

* Usuário

* Dependente

* Broker

### Precondições

* O ator Usuário ou Dependente deve estar autenticado no sistema.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário ou Dependente acessa a seção de Módulos.

2. O ator Broker envia os últimos estados dos módulos.

3. O sistema apresenta os últimos estados dos módulos.

### Pontos de Inclusão

#### Comunicar por MQTT

O sistema deve realizar a conexão com o ator Broker por MQTT e, em seguida, **Inscrever Usuários** nos tópicos relacionados aos módulos do mesmo.

## Solicitar Ajuda

### Resumo

Em caso de emergência, o usuário envia uma mensagem para os contatos de emergência cadastrados, assim, solicitando ajuda.

### Atores

### Precondições

* O ator Usuário deve estar autenticado do sistema.

* O ator Usuário deve ter Contatos de Emergência ou Usuários Dependentes cadastrados no sistema.

### Pós-condições

* Os Contatos de Emergência e/ou Usuários Dependentes devem receber a mensagem pelos meios disponíveis.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Usuário aciona a ação Solicitar Ajuda.

2. O sistema pergunta a mensagem a ser enviada.

3. O ator Usuário preenche a mensagem e confirma a operação.

4. O sistema envia a mensagem para os Contatos de Emergência e/ou Usuários Dependentes pelos meios disponíveis.

#### Fluxos Alternativos

##### 3a: Usuário não respondeu por x segundos

1. O sistema continua a operação com uma mensagem padrão.

### Pontos de Extensão

#### Enviar mensagem pelo Facebook

O sistema envia a mensagem para os Contatos de Emergência e Usuários Dependentes com Facebook cadastrado.

#### Enviar mensagem pelo Twitter

O sistema envia a mensagem para os Contatos de Emergência e Usuários Dependentes com Twitter cadastrado.

#### Enviar email

O sistema transforma a mensagem em email e envia para os Contatos de Emergência e Usuários Dependentes.

### Pontes de Inclusão

#### Enviar mensagem pelo sistema

O sistema propaga a mensagem para os Usuários Dependentes.

## Gerenciar Tipos de Módulos

### Resumo

O administrador visualiza, edita, adiciona ou exclui tipos de módulos no sistema.

### Atores

* Administrador

### Precondições

* O ator Administrador deve estar autenticado no sistema.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Administrador acessa a seção de Tipos de Módulos.

2. O ator Administrador decide adicionar, editar ou excluir.

3. O ator Administrador acessa o formulário de Tipo de Módulo.

4. O ator Administrador realiza as modificações.

5. O ator Administrador salva as modificações.

## Gerenciar Módulos Disponíveis

### Resumo

O administrador gerencia os módulos disponíveis para serem adquiridos pelos usuários.

### Atores

* Administrador

### Precondições

* O ator Administrador deve estar autenticado no sistema.

### Pós-condições

* Quando adicionado, o módulo deve ficar disponível para outros atores (Usuário e Dependente) realizarem a ativação.

### Fluxos de Evento

#### Fluxo Básico

1. O ator Administrador acessa a seção de Módulos Disponíveis.

2. O ator Administrador decide adicionar, editar ou excluir.

3. O ator Administrador acessa o formulário de Módulo Disponível.

4. O ator Administrador realiza as modificações.

5. O ator Administrador salva as modificações.
