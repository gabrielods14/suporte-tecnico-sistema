// src/pages/FAQPage.jsx
import React, { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import '../styles/faq.css';
import { 
  FaHome, 
  FaClipboardList, 
  FaEdit, 
  FaCheckCircle, 
  FaChartBar, 
  FaUserPlus, 
  FaUserCircle,
  FaQuestionCircle,
  FaChevronDown,
  FaChevronUp,
  FaInfoCircle,
  FaExclamationCircle,
  FaLightbulb
} from 'react-icons/fa';

function FAQPage({ onLogout, onNavigateToHome, onNavigateToPage, currentPage, userInfo, onNavigateToProfile }) {
  const [openSection, setOpenSection] = useState(null);
  const firstName = userInfo?.nome?.split(' ')[0] || 'Usuário';
  const permissao = userInfo?.permissao; // 3=Admin, 2=SuporteTecnico, 1=Colaborador

  const toggleSection = (sectionId) => {
    setOpenSection(openSection === sectionId ? null : sectionId);
  };

  // Determina se o usuário é apenas colaborador (sem permissões de suporte/admin)
  const isColaborador = permissao === 1 || permissao == null;

  const faqSections = [
    {
      id: 'visao-geral',
      title: 'Visão Geral do Sistema',
      icon: <FaInfoCircle />,
      content: (
        <div>
          <p className="intro-text">
            O <strong>HelpWave</strong> é um sistema de gestão de chamados técnicos desenvolvido para facilitar 
            a comunicação entre colaboradores e a equipe de suporte técnico. Este manual irá guiá-lo através 
            de todas as funcionalidades disponíveis.
          </p>
          {!isColaborador && (
            <div className="info-box">
              <strong>Tipos de Usuário:</strong>
              <ul>
                <li><strong>Colaborador (Permissão 1):</strong> Pode criar chamados e visualizar seus próprios chamados.</li>
                <li><strong>Suporte Técnico (Permissão 2):</strong> Pode visualizar, gerenciar e resolver chamados de todos os usuários.</li>
                <li><strong>Administrador (Permissão 3):</strong> Tem acesso completo, incluindo cadastro de funcionários e relatórios detalhados.</li>
              </ul>
            </div>
          )}
          {isColaborador && (
            <div className="info-box">
              <strong>Sua Conta:</strong>
              <p>Você está logado como <strong>Colaborador</strong>. Com essa permissão, você pode:</p>
              <ul>
                <li>Criar novos chamados técnicos quando precisar de assistência</li>
                <li>Visualizar e acompanhar seus chamados</li>
                <li>Gerenciar suas informações de perfil</li>
              </ul>
              <p>Para funcionalidades adicionais, entre em contato com um administrador do sistema.</p>
            </div>
          )}
        </div>
      )
    },
    {
      id: 'navegacao',
      title: 'Navegação no Sistema',
      icon: <FaHome />,
      content: (
        <div>
          <h4>Menu Lateral (Sidebar)</h4>
          <p>O menu lateral está sempre visível e permite acesso rápido às principais áreas do sistema:</p>
          <ul className="feature-list">
            <li><strong>HOME:</strong> Retorna à página inicial com os cards de acesso rápido</li>
            {!isColaborador && (
              <>
                <li><strong>CHAMADO:</strong> Visualiza chamados em andamento (Suporte e Admin)</li>
                <li><strong>RELATÓRIOS:</strong> Acessa estatísticas e relatórios (Suporte e Admin)</li>
              </>
            )}
            <li><strong>FQA:</strong> Esta página de ajuda e manual do sistema</li>
            <li><strong>CONTATO:</strong> Informações de contato para suporte adicional</li>
          </ul>
          
          <h4>Header (Cabeçalho)</h4>
          <ul className="feature-list">
            <li><strong>Ícone de Usuário:</strong> Clique para acessar seu perfil</li>
            <li><strong>Ícone de Engrenagem:</strong> Menu com opções de Perfil e Logout</li>
          </ul>
        </div>
      )
    },
    {
      id: 'home',
      title: 'Página Inicial (Home)',
      icon: <FaHome />,
      content: (
        <div>
          <p>A página inicial exibe cards clicáveis que levam às principais funcionalidades disponíveis para você:</p>
          
          <div className="card-info">
            <h4><FaEdit /> NOVO CHAMADO</h4>
            <p><strong>Funcionalidade:</strong> Permite criar um novo chamado técnico quando você precisar de assistência. Você precisa informar:</p>
            <ul>
              <li>Tipo de chamado (Suporte, Manutenção, Instalação, Consultoria, Emergência)</li>
              <li>Título do chamado</li>
              <li>Descrição detalhada do problema</li>
            </ul>
            <p className="tip"><FaLightbulb /> <strong>Dica:</strong> Seja específico na descrição para facilitar o atendimento da equipe de suporte.</p>
          </div>

          {!isColaborador && (
            <>
              <div className="card-info">
                <h4><FaClipboardList /> CHAMADOS EM ANDAMENTO</h4>
                <p><strong>Disponível para:</strong> Suporte Técnico e Administrador</p>
                <p><strong>Funcionalidade:</strong> Lista todos os chamados que estão abertos ou em andamento. Você pode:</p>
                <ul>
                  <li>Visualizar lista de chamados pendentes</li>
                  <li>Filtrar e buscar chamados</li>
                  <li>Clicar em um chamado para ver detalhes e atualizar</li>
                </ul>
              </div>

              <div className="card-info">
                <h4><FaCheckCircle /> CHAMADOS CONCLUÍDOS</h4>
                <p><strong>Disponível para:</strong> Suporte Técnico e Administrador</p>
                <p><strong>Funcionalidade:</strong> Histórico de todos os chamados já resolvidos.</p>
              </div>

              <div className="card-info">
                <h4><FaChartBar /> RELATÓRIOS</h4>
                <p><strong>Disponível para:</strong> Suporte Técnico e Administrador</p>
                <p><strong>Funcionalidade:</strong> Visualiza estatísticas e métricas do sistema.</p>
              </div>

              {permissao === 3 && (
                <div className="card-info">
                  <h4><FaUserPlus /> CADASTRO DE FUNCIONÁRIO</h4>
                  <p><strong>Disponível para:</strong> Apenas Administrador</p>
                  <p><strong>Funcionalidade:</strong> Permite cadastrar novos usuários no sistema com diferentes níveis de permissão.</p>
                </div>
              )}
            </>
          )}

          {isColaborador && (
            <div className="info-box">
              <strong>Você é Colaborador:</strong>
              <p>Como colaborador, você tem acesso ao card <strong>"NOVO CHAMADO"</strong> para solicitar assistência técnica sempre que precisar.</p>
              <p>Após criar um chamado, a equipe de suporte entrará em contato para ajudá-lo a resolver o problema.</p>
            </div>
          )}
        </div>
      )
    },
    {
      id: 'criar-chamado',
      title: 'Como Criar um Chamado',
      icon: <FaEdit />,
      content: (
        <div>
          <ol className="step-list">
            <li>Na página inicial, clique no card <strong>"NOVO CHAMADO"</strong></li>
            <li>Selecione o <strong>Tipo de Chamado</strong> no dropdown:
              <ul>
                <li><strong>Suporte:</strong> Para dúvidas e assistência técnica</li>
                <li><strong>Manutenção:</strong> Para reparos e ajustes</li>
                <li><strong>Instalação:</strong> Para instalação de novos equipamentos/softwares</li>
                <li><strong>Consultoria:</strong> Para orientações e consultas</li>
                <li><strong>Emergência:</strong> Para problemas críticos que precisam de atenção imediata</li>
              </ul>
            </li>
            <li>Digite um <strong>Título</strong> descritivo para o chamado (mínimo 5 caracteres)</li>
            <li>Escreva uma <strong>Descrição</strong> detalhada do problema, incluindo:
              <ul>
                <li>O que está acontecendo</li>
                <li>Quando começou o problema</li>
                <li>Passos que já foram tentados para resolver</li>
                <li>Qualquer mensagem de erro ou comportamento inesperado</li>
              </ul>
            </li>
            <li>Clique em <strong>"CRIAR CHAMADO"</strong></li>
          </ol>
          <div className="warning-box">
            <FaExclamationCircle /> <strong>Atenção:</strong> Certifique-se de preencher todos os campos obrigatórios antes de enviar.
          </div>
        </div>
      )
    },
    {
      id: 'gerenciar-chamados',
      title: 'Gerenciar Chamados (Suporte/Admin)',
      icon: <FaClipboardList />,
      visibleFor: [2, 3], // Apenas Suporte e Admin
      content: (
        <div>
          <h4>Visualizar Chamados em Andamento</h4>
          <ol className="step-list">
            <li>Acesse <strong>"CHAMADOS EM ANDAMENTO"</strong> pelo menu lateral ou card na home</li>
            <li>Você verá uma lista com:
              <ul>
                <li>Código do chamado</li>
                <li>Título</li>
                <li>Status (Aberto, Em Andamento, etc.)</li>
                <li>Prioridade</li>
                <li>Data de criação</li>
                <li>Data limite (se aplicável)</li>
              </ul>
            </li>
            <li>Use a <strong>barra de pesquisa</strong> para buscar por título ou código</li>
            <li>Use os <strong>filtros</strong> para ordenar por diferentes critérios</li>
            <li><strong>Clique em um chamado</strong> para ver detalhes completos</li>
          </ol>

          <h4>Atualizar um Chamado</h4>
          <ol className="step-list">
            <li>Ao abrir um chamado, você verá todas as informações</li>
            <li>Na seção de <strong>"Solução"</strong>, você pode:
              <ul>
                <li>Escrever a descrição da solução aplicada</li>
                <li>Usar o <strong>botão "Gerar Sugestão com IA"</strong> para obter uma sugestão automática baseada no problema</li>
              </ul>
            </li>
            <li>Altere o <strong>Status</strong> do chamado conforme o progresso:
              <ul>
                <li><strong>Aberto:</strong> Chamado recém-criado</li>
                <li><strong>Em Andamento:</strong> Chamado sendo trabalhado</li>
                <li><strong>Resolvido:</strong> Problema solucionado</li>
              </ul>
            </li>
            <li>Clique em <strong>"SALVAR ALTERAÇÕES"</strong> para atualizar o chamado</li>
          </ol>

          <div className="tip-box">
            <FaLightbulb /> <strong>Dica:</strong> A IA pode ajudar a gerar respostas profissionais para os chamados. 
            Experimente usar a função "Gerar Sugestão com IA"!
          </div>
        </div>
      )
    },
    {
      id: 'relatorios',
      title: 'Relatórios e Estatísticas',
      icon: <FaChartBar />,
      visibleFor: [2, 3], // Apenas Suporte e Admin
      content: (
        <div>
          <p>Os relatórios fornecem uma visão geral do desempenho do sistema:</p>
          <ul className="feature-list">
            <li><strong>Total de Usuários:</strong> Número total de usuários cadastrados</li>
            <li><strong>Total de Chamados:</strong> Todos os chamados já criados</li>
            <li><strong>Chamados Resolvidos:</strong> Quantidade de chamados já concluídos</li>
            <li><strong>Chamados Em Andamento:</strong> Chamados abertos que estão sendo trabalhados</li>
          </ul>
          <p className="note-text">Disponível apenas para Suporte Técnico e Administradores.</p>
        </div>
      )
    },
    {
      id: 'perfil',
      title: 'Gerenciar Perfil',
      icon: <FaUserCircle />,
      content: (
        <div>
          <h4>Como Acessar Seu Perfil</h4>
          <ol className="step-list">
            <li>Clique no <strong>ícone de usuário</strong> no header, OU</li>
            <li>Clique no <strong>ícone de engrenagem</strong> e selecione <strong>"Perfil"</strong> no menu</li>
          </ol>

          <h4>Editar Informações do Perfil</h4>
          <ol className="step-list">
            <li>Na página de perfil, clique no botão <strong>"EDITAR PERFIL"</strong></li>
            <li>Os campos editáveis serão habilitados:
              <ul>
                <li><strong>Nome Completo:</strong> Seu nome no sistema</li>
                <li><strong>E-mail:</strong> Seu endereço de e-mail de contato</li>
                <li><strong>Cargo:</strong> Seu cargo/função na empresa</li>
                <li><strong>Telefone:</strong> Seu número de telefone (opcional)</li>
              </ul>
            </li>
            <li>Faça as alterações desejadas</li>
            <li>Clique em <strong>"SALVAR ALTERAÇÕES"</strong> para confirmar</li>
            <li>Ou clique em <strong>"CANCELAR"</strong> para descartar as mudanças</li>
          </ol>

          <div className="info-box">
            <strong>Nota:</strong> A senha e permissões não podem ser alteradas pela página de perfil. 
            Entre em contato com um administrador se precisar alterar essas informações.
          </div>
        </div>
      )
    },
    {
      id: 'cadastro-usuario',
      title: 'Cadastrar Funcionário (Admin)',
      icon: <FaUserPlus />,
      visibleFor: [3], // Apenas Admin
      content: (
        <div>
          <p className="note-text"><strong>Disponível apenas para Administradores</strong></p>
          <ol className="step-list">
            <li>Acesse <strong>"CADASTRO DE FUNCIONÁRIO"</strong> pelo card na página inicial</li>
            <li>Preencha os dados do novo funcionário:
              <ul>
                <li><strong>Nome Completo:</strong> Nome completo do funcionário</li>
                <li><strong>E-mail:</strong> E-mail que será usado para login</li>
                <li><strong>Cargo:</strong> Cargo/função do funcionário</li>
                <li><strong>Telefone:</strong> Número de telefone (opcional)</li>
                <li><strong>Senha:</strong> Senha inicial (mínimo 6 caracteres)</li>
                <li><strong>Permissão:</strong> Selecione o nível de acesso:
                  <ul>
                    <li><strong>Colaborador:</strong> Pode apenas criar chamados</li>
                    <li><strong>Suporte Técnico:</strong> Pode gerenciar chamados</li>
                    <li><strong>Administrador:</strong> Acesso completo ao sistema</li>
                  </ul>
                </li>
              </ul>
            </li>
            <li>Clique em <strong>"CADASTRAR"</strong></li>
          </ol>
          <div className="warning-box">
            <FaExclamationCircle /> <strong>Importante:</strong> Escolha cuidadosamente o nível de permissão ao cadastrar um usuário.
          </div>
        </div>
      )
    },
    {
      id: 'perguntas-frequentes',
      title: 'Perguntas Frequentes',
      icon: <FaQuestionCircle />,
      content: (
        <div>
          <div className="faq-item">
            <h4>Como faço login no sistema?</h4>
            <p>Use seu e-mail e senha cadastrados. Se você não tem acesso, entre em contato com um administrador.</p>
          </div>

          <div className="faq-item">
            <h4>Esqueci minha senha. O que fazer?</h4>
            <p>Entre em contato com o administrador do sistema ou com a equipe de TI para redefinir sua senha.</p>
          </div>

          <div className="faq-item">
            <h4>Posso cancelar um chamado que criei?</h4>
            <p>Chamados abertos podem ser atualizados apenas pela equipe de suporte. Se precisar cancelar, entre em contato com a equipe.</p>
          </div>

          <div className="faq-item">
            <h4>Como sei quando meu chamado foi resolvido?</h4>
            <p>O status do chamado será atualizado para "Resolvido" quando o técnico finalizar o atendimento. {isColaborador ? 'A equipe de suporte entrará em contato quando o problema for resolvido.' : 'Você pode acompanhar pelo status.'}</p>
          </div>

          {!isColaborador && (
            <div className="faq-item">
              <h4>O que é a função de IA nos chamados?</h4>
              <p>A IA (Inteligência Artificial) ajuda a equipe de suporte a gerar sugestões de resposta profissional baseadas na descrição do problema do chamado.</p>
            </div>
          )}

          <div className="faq-item">
            <h4>Posso anexar arquivos aos chamados?</h4>
            <p>Atualmente, o sistema permite apenas texto na descrição. Para compartilhar arquivos, mencione-os na descrição ou entre em contato diretamente com o suporte.</p>
          </div>

          <div className="faq-item">
            <h4>Como altero minha senha?</h4>
            <p>Atualmente, a alteração de senha deve ser solicitada ao administrador. Entre em contato com a equipe de TI.</p>
          </div>
        </div>
      )
    },
    {
      id: 'dicas-uso',
      title: 'Dicas de Uso',
      icon: <FaLightbulb />,
      content: (
        <div>
          <div className="tip-box">
            <FaLightbulb /> <strong>Seja Descritivo:</strong> Ao criar um chamado, forneça o máximo de informações possível. 
            Isso ajuda a equipe a resolver mais rapidamente.
          </div>

          <div className="tip-box">
            <FaLightbulb /> <strong>Verifique Status Regularmente:</strong> Acompanhe o status dos seus chamados para estar sempre atualizado.
          </div>

          {!isColaborador && (
            <div className="tip-box">
              <FaLightbulb /> <strong>Use os Filtros:</strong> Se você é técnico, use os filtros na lista de chamados para organizar melhor seu trabalho.
            </div>
          )}

          <div className="tip-box">
            <FaLightbulb /> <strong>Atualize Seu Perfil:</strong> Mantenha suas informações de contato atualizadas para facilitar a comunicação.
          </div>

          {!isColaborador && (
            <div className="tip-box">
              <FaLightbulb /> <strong>Explore a IA:</strong> Se você é técnico, experimente a função de sugestão de IA para respostas mais rápidas e profissionais.
            </div>
          )}

          {isColaborador && (
            <div className="tip-box">
              <FaLightbulb /> <strong>Aguarde o Atendimento:</strong> Após criar seu chamado, aguarde que a equipe de suporte entre em contato para resolver sua solicitação.
            </div>
          )}
        </div>
      )
    }
  ];

  return (
    <div className="faq-layout">
      <Header onLogout={onLogout} userName={firstName} onNavigateToProfile={onNavigateToProfile} />
      <Sidebar currentPage={currentPage} onNavigate={onNavigateToPage} />
      
      <main className="faq-main-content">
        <div className="faq-header">
          <h1>
            <FaQuestionCircle className="faq-title-icon" />
            Manual do Sistema HelpWave
          </h1>
          <p className="faq-subtitle">Guia completo para uso do sistema de gestão de chamados técnicos</p>
        </div>

        <div className="faq-content">
          {faqSections
            .filter((section) => {
              // Se não tem restrição de visibilidade, mostra para todos
              if (!section.visibleFor) return true;
              // Se tem restrição, verifica se o usuário tem permissão
              return section.visibleFor.includes(permissao);
            })
            .map((section) => (
            <div key={section.id} className="faq-section">
              <button
                className={`faq-section-header ${openSection === section.id ? 'open' : ''}`}
                onClick={() => toggleSection(section.id)}
              >
                <span className="faq-section-title">
                  <span className="faq-section-icon">{section.icon}</span>
                  {section.title}
                </span>
                {openSection === section.id ? (
                  <FaChevronUp className="faq-chevron" />
                ) : (
                  <FaChevronDown className="faq-chevron" />
                )}
              </button>
              {openSection === section.id && (
                <div className="faq-section-content">
                  {section.content}
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="faq-footer">
          <p>Não encontrou o que procura? Entre em contato através do menu <strong>CONTATO</strong>.</p>
          <p className="faq-copyright">© 2025 HelpWave - Simplificando o seu suporte</p>
        </div>
      </main>
    </div>
  );
}

export default FAQPage;

