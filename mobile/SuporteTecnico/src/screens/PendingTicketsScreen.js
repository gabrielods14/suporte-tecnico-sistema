import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  ScrollView,
  StatusBar,
  Alert,
  TextInput,
  Modal,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useTickets } from '../context/TicketContext';
import AIService from '../services/AIService';
import ConfirmationModal from '../components/ConfirmationModal';
import Toast from '../components/Toast';
import LoadingOverlay from '../components/LoadingOverlay';

const PendingTicketsScreen = ({ navigation }) => {
  const { tickets, loadTickets, respondToTicket, completeTicket, setAISuggestion, loading, error } = useTickets();
  const [selectedTicket, setSelectedTicket] = useState(null);
  const [responseText, setResponseText] = useState('');
  const [isResponseModalOpen, setIsResponseModalOpen] = useState(false);
  const [isAILoading, setIsAILoading] = useState(false);
  const [aiSuggestion, setAiSuggestion] = useState(null);
  const [aiResponseText, setAiResponseText] = useState('');
  const [useAISuggestion, setUseAISuggestion] = useState(false);
  const [showCompleteModal, setShowCompleteModal] = useState(false);
  const [ticketToComplete, setTicketToComplete] = useState(null);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');
  const [showFinalizeModal, setShowFinalizeModal] = useState(false);
  const [ticketToFinalize, setTicketToFinalize] = useState(null);

  useEffect(() => {
    // Carregar tickets quando a tela é montada
    loadTickets();
  }, []);

  // Recarregar tickets quando a tela recebe foco (quando o usuário navega para ela)
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      loadTickets();
    });
    return unsubscribe;
  }, [navigation]);

  // Filtrar tickets em andamento e abertos
  // Status possíveis: 'Aberto' (1), 'Em Atendimento' (2), 'Fechado' (3)
  const pendingTickets = tickets.filter(ticket => 
    ticket.status === 'Em Atendimento' || 
    ticket.status === 'Em andamento' || // Compatibilidade com formato antigo
    ticket.status === 'Aberto'
  );

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Alta': return '#dc3545';
      case 'Média': return '#ffc107';
      case 'Baixa': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Aberto': return '#007bff';
      case 'Em Atendimento':
      case 'Em andamento': // Compatibilidade com formato antigo
        return '#ffc107';
      case 'Fechado': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Aberto': return 'alert-circle-outline';
      case 'Em Atendimento':
      case 'Em andamento': // Compatibilidade com formato antigo
        return 'time-outline';
      case 'Fechado': return 'checkmark-circle-outline';
      default: return 'help-circle-outline';
    }
  };

  const getProblemTypeIcon = (type) => {
    const icons = {
      hardware: 'hardware-chip-outline',
      software: 'desktop-outline',
      network: 'wifi-outline',
      printer: 'print-outline',
      email: 'mail-outline',
      password: 'key-outline',
      access: 'lock-closed-outline',
      other: 'help-circle-outline',
    };
    return icons[type] || 'help-circle-outline';
  };

  const handleGetAISuggestion = async (ticket) => {
    setIsAILoading(true);
    try {
      const suggestion = await AIService.getSuggestion(ticket.type, ticket.description);
      setAiSuggestion(suggestion);
      setAISuggestion(ticket.id, JSON.stringify(suggestion));
    } catch (error) {
      Alert.alert('Erro', 'Não foi possível obter sugestão da IA');
    } finally {
      setIsAILoading(false);
    }
  };

      const generateAutoResponse = (suggestion, ticket) => {
        if (!suggestion || !suggestion.stepByStepSolution) {
          return 'Problema analisado e solução técnica aplicada com sucesso.';
        }

        // Criar resposta técnica baseada no passo-a-passo específico
        const stepByStepResponse = suggestion.stepByStepSolution.slice(0, 2).join(' ');
        
        // Adicionar informações de verificação se disponíveis
        let verificationInfo = '';
        if (suggestion.verificationSteps && suggestion.verificationSteps.length > 0) {
          verificationInfo = ` Verificação realizada: ${suggestion.verificationSteps[0]}`;
        }

        // Adicionar informações de comandos específicos se disponíveis
        let commandInfo = '';
        if (suggestion.specificCommands && suggestion.specificCommands.length > 0) {
          commandInfo = ` Comandos executados: ${suggestion.specificCommands[0]}`;
        }

        // Adicionar causa raiz se disponível
        let rootCauseInfo = '';
        if (suggestion.rootCause) {
          rootCauseInfo = ` Causa identificada: ${suggestion.rootCause}`;
        }

        return `SOLUÇÃO TÉCNICA APLICADA: ${stepByStepResponse}.${rootCauseInfo}${commandInfo}${verificationInfo} Problema resolvido com sucesso.`;
      };


  const handleFinalizeTicket = () => {
    setTicketToFinalize(selectedTicket);
    setShowFinalizeModal(true);
  };

  const confirmFinalizeTicket = () => {
    if (ticketToFinalize) {
      // Simular nome do técnico logado (em produção viria do contexto de autenticação)
      const technicianName = 'Técnico Atual';
      
      // Adicionar resposta antes de finalizar
      const finalResponseText = useAISuggestion ? aiResponseText : responseText;
      if (finalResponseText.trim()) {
        respondToTicket(ticketToFinalize.id, finalResponseText.trim(), technicianName);
      }
      
      // Finalizar o chamado
      completeTicket(ticketToFinalize.id, technicianName);
      
      // Limpar estados
      setResponseText('');
      setAiResponseText('');
      setUseAISuggestion(false);
      setAiSuggestion(null);
      setIsResponseModalOpen(false);
      setSelectedTicket(null);
      loadTickets();
      setShowFinalizeModal(false);
      setTicketToFinalize(null);
      showToastMessage('Chamado finalizado com sucesso!', 'success');
    }
  };

  const handleCompleteTicket = (ticket) => {
    setTicketToComplete(ticket);
    setShowCompleteModal(true);
  };

  const showToastMessage = (message, type = 'success') => {
    setToastMessage(message);
    setToastType(type);
    setShowToast(true);
  };

  const confirmCompleteTicket = () => {
    if (ticketToComplete) {
      // Simular nome do técnico logado (em produção viria do contexto de autenticação)
      const technicianName = 'Técnico Atual';
      
      completeTicket(ticketToComplete.id, technicianName);
      loadTickets();
      setShowCompleteModal(false);
      setTicketToComplete(null);
      showToastMessage('Chamado finalizado com sucesso!', 'success');
    }
  };

  const renderTicketItem = ({ item: ticket }) => (
    <TouchableOpacity
      style={styles.ticketCard}
      onPress={async () => {
        setSelectedTicket(ticket);
        setIsResponseModalOpen(true);
        
        // Buscar sugestão da IA automaticamente
        setIsAILoading(true);
        try {
          const suggestion = await AIService.getSuggestion(ticket.type, ticket.description);
          setAiSuggestion(suggestion);
          setAISuggestion(ticket.id, JSON.stringify(suggestion));
          
          // Gerar resposta automática baseada na sugestão
          const autoResponse = generateAutoResponse(suggestion, ticket);
          setAiResponseText(autoResponse);
        } catch (error) {
          Alert.alert('Erro', 'Não foi possível obter sugestão da IA');
        } finally {
          setIsAILoading(false);
        }
      }}
    >
      <View style={styles.ticketHeader}>
        <View style={styles.ticketInfo}>
          <Text style={styles.ticketTitle}>{ticket.title}</Text>
          <Text style={styles.ticketUser}>Por: {ticket.user}</Text>
          <Text style={styles.ticketDate}>{ticket.createdAt}</Text>
        </View>
        <Icon name="chevron-forward" size={20} color="#666" />
      </View>

      <View style={styles.ticketDescription}>
        <Text style={styles.descriptionText} numberOfLines={2}>
          {ticket.description}
        </Text>
      </View>

      <View style={styles.ticketBadges}>
        <View style={[styles.badge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
          <Text style={styles.badgeText}>{ticket.priority}</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: getStatusColor(ticket.status) }]}>
          <Icon name={getStatusIcon(ticket.status)} size={12} color="#fff" style={styles.badgeIcon} />
          <Text style={styles.badgeText}>{ticket.status}</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: '#6c757d' }]}>
          <Icon name={getProblemTypeIcon(ticket.type)} size={12} color="#fff" style={styles.badgeIcon} />
          <Text style={styles.badgeText}>{ticket.type}</Text>
        </View>
      </View>

      <View style={styles.ticketActions}>
        <TouchableOpacity
          style={styles.actionButton}
          onPress={() => handleGetAISuggestion(ticket)}
        >
          <Icon name="bulb-outline" size={16} color="#ffc107" />
          <Text style={styles.actionButtonText}>IA</Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#dc3545" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={() => navigation.goBack()}
        >
          <Icon name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Chamados em Andamento</Text>
        <TouchableOpacity 
          style={styles.refreshButton}
          onPress={loadTickets}
        >
          <Icon name="refresh-outline" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Tickets List */}
      <FlatList
        data={pendingTickets}
        keyExtractor={(item) => item.id}
        renderItem={renderTicketItem}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="checkmark-circle-outline" size={64} color="#28a745" />
            <Text style={styles.emptyTitle}>Nenhum chamado em andamento</Text>
            <Text style={styles.emptySubtitle}>
              Todos os chamados foram resolvidos! 🎉
            </Text>
          </View>
        }
      />

      {/* Response Modal */}
      <Modal
        visible={isResponseModalOpen}
        transparent={true}
        animationType="slide"
        onRequestClose={() => setIsResponseModalOpen(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Responder ao Chamado</Text>
              <TouchableOpacity onPress={() => setIsResponseModalOpen(false)}>
                <Icon name="close-outline" size={24} color="#666" />
              </TouchableOpacity>
            </View>

            {selectedTicket && (
              <ScrollView style={styles.modalBody}>
                <View style={styles.ticketDetails}>
                  <Text style={styles.detailTitle}>{selectedTicket.title}</Text>
                  <Text style={styles.detailUser}>Por: {selectedTicket.user}</Text>
                  <Text style={styles.detailDescription}>{selectedTicket.description}</Text>
                </View>

                    {/* AI Suggestion */}
                    {selectedTicket.aiSuggestion && (
                      <View style={styles.aiSuggestion}>
                        <View style={styles.aiHeader}>
                          <Icon name="bulb-outline" size={20} color="#ffc107" />
                          <Text style={styles.aiTitle}>Análise Técnica Detalhada</Text>
                        </View>
                        {(() => {
                          try {
                            const suggestion = JSON.parse(selectedTicket.aiSuggestion);
                            return (
                              <View>
                                <Text style={styles.aiAnalysis}>{suggestion.analysis}</Text>
                                
                                {/* Sintomas Identificados */}
                                {suggestion.symptoms && suggestion.symptoms.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>🔍 Sintomas Identificados:</Text>
                                    {suggestion.symptoms.map((symptom, index) => (
                                      <Text key={index} style={styles.aiStep}>• {symptom}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Causa Raiz */}
                                {suggestion.rootCause && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>🎯 Causa Raiz:</Text>
                                    <Text style={styles.aiRootCause}>{suggestion.rootCause}</Text>
                                  </View>
                                )}

                                {/* Passo-a-Passo da Solução */}
                                {suggestion.stepByStepSolution && suggestion.stepByStepSolution.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>📋 Passo-a-Passo da Solução:</Text>
                                    {suggestion.stepByStepSolution.map((step, index) => (
                                      <Text key={index} style={styles.aiStepNumber}>
                                        {index + 1}. {step}
                                      </Text>
                                    ))}
                                  </View>
                                )}

                                {/* Comandos Específicos */}
                                {suggestion.specificCommands && suggestion.specificCommands.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>💻 Comandos Específicos:</Text>
                                    {suggestion.specificCommands.map((command, index) => (
                                      <Text key={index} style={styles.aiCommandStep}>• {command}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Arquivos de Configuração */}
                                {suggestion.configurationFiles && suggestion.configurationFiles.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>📁 Arquivos de Configuração:</Text>
                                    {suggestion.configurationFiles.map((file, index) => (
                                      <Text key={index} style={styles.aiConfigStep}>• {file}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Logs para Verificar */}
                                {suggestion.logsToCheck && suggestion.logsToCheck.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>📋 Logs para Verificar:</Text>
                                    {suggestion.logsToCheck.map((log, index) => (
                                      <Text key={index} style={styles.aiLogStep}>• {log}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Ferramentas Necessárias */}
                                {suggestion.toolsNeeded && suggestion.toolsNeeded.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>🔧 Ferramentas Necessárias:</Text>
                                    {suggestion.toolsNeeded.map((tool, index) => (
                                      <Text key={index} style={styles.aiToolStep}>• {tool}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Problemas Comuns */}
                                {suggestion.commonIssues && suggestion.commonIssues.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>⚠️ Problemas Comuns:</Text>
                                    {suggestion.commonIssues.map((issue, index) => (
                                      <Text key={index} style={styles.aiErrorStep}>• {issue}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Verificação */}
                                {suggestion.verificationSteps && suggestion.verificationSteps.length > 0 && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>✅ Verificação:</Text>
                                    {suggestion.verificationSteps.map((step, index) => (
                                      <Text key={index} style={styles.aiStep}>• {step}</Text>
                                    ))}
                                  </View>
                                )}

                                {/* Informações Adicionais */}
                                {suggestion.additional && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>ℹ️ Informações Adicionais:</Text>
                                    <Text style={styles.aiAdditional}>{suggestion.additional}</Text>
                                  </View>
                                )}

                                {/* Critérios de Escalação */}
                                {suggestion.escalationCriteria && (
                                  <View style={styles.aiSection}>
                                    <Text style={styles.aiSectionTitle}>🚨 Escalação:</Text>
                                    <Text style={styles.aiEscalation}>{suggestion.escalationCriteria}</Text>
                                  </View>
                                )}

                                {/* Metadados */}
                                <View style={styles.aiMetadata}>
                                  <Text style={styles.aiConfidence}>Confiança: {suggestion.confidence}</Text>
                                  <Text style={styles.aiTime}>Tempo estimado: {suggestion.estimatedTime}</Text>
                                  <Text style={styles.aiPriority}>Prioridade: {suggestion.priority}</Text>
                                </View>
                              </View>
                            );
                          } catch {
                            return <Text style={styles.aiText}>{selectedTicket.aiSuggestion}</Text>;
                          }
                        })()}
                      </View>
                    )}

                <View style={styles.responseSection}>
                  <Text style={styles.responseLabel}>Sua resposta:</Text>
                  
                  {/* Opção de usar sugestão da IA */}
                  {aiSuggestion && (
                    <View style={styles.aiResponseOption}>
                      <TouchableOpacity
                        style={styles.aiToggleButton}
                        onPress={() => setUseAISuggestion(!useAISuggestion)}
                      >
                        <Icon 
                          name={useAISuggestion ? "checkmark-circle" : "ellipse-outline"} 
                          size={20} 
                          color={useAISuggestion ? "#28a745" : "#666"} 
                        />
                        <Text style={styles.aiToggleText}>Usar sugestão da IA</Text>
                      </TouchableOpacity>
                      
                      {useAISuggestion && (
                        <View style={styles.aiResponsePreview}>
                          <Text style={styles.aiResponseLabel}>Resposta gerada pela IA:</Text>
                          <Text style={styles.aiResponseText}>{aiResponseText}</Text>
                        </View>
                      )}
                    </View>
                  )}
                  
                  {/* Campo de resposta manual */}
                  {!useAISuggestion && (
                    <TextInput
                      style={styles.responseInput}
                      placeholder="Descreva o que foi feito para resolver o problema..."
                      placeholderTextColor="#999"
                      value={responseText}
                      onChangeText={setResponseText}
                      multiline
                      numberOfLines={4}
                      textAlignVertical="top"
                    />
                  )}
                  
                  {/* Loading da IA */}
                  {isAILoading && (
                    <View style={styles.aiLoading}>
                      <Icon name="bulb-outline" size={20} color="#ffc107" />
                      <Text style={styles.aiLoadingText}>IA analisando o problema...</Text>
                    </View>
                  )}
                </View>
              </ScrollView>
            )}

            <View style={styles.modalFooter}>
              <TouchableOpacity
                style={styles.cancelButton}
                onPress={() => setIsResponseModalOpen(false)}
              >
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              <TouchableOpacity
                style={styles.finalizeButton}
                onPress={handleFinalizeTicket}
              >
                <Text style={styles.finalizeButtonText}>Finalizar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* Complete Ticket Confirmation Modal */}
      <ConfirmationModal
        visible={showCompleteModal}
        onClose={() => setShowCompleteModal(false)}
        onConfirm={confirmCompleteTicket}
        title="Finalizar Chamado"
        message={`Tem certeza que deseja finalizar o chamado "${ticketToComplete?.title}"? Esta ação não pode ser desfeita e o chamado será marcado como concluído.`}
        confirmText="Finalizar"
        cancelText="Cancelar"
        confirmColor="#28a745"
        iconName="checkmark-circle-outline"
        iconColor="#28a745"
        type="info"
      />

      {/* Finalize Ticket Confirmation Modal */}
      <ConfirmationModal
        visible={showFinalizeModal}
        onClose={() => setShowFinalizeModal(false)}
        onConfirm={confirmFinalizeTicket}
        title="Finalizar Chamado"
        message={`Tem certeza que deseja finalizar o chamado "${ticketToFinalize?.title}"? A resposta será enviada e o chamado será marcado como concluído. Esta ação não pode ser desfeita.`}
        confirmText="Sim, Finalizar"
        cancelText="Não, Continuar Editando"
        confirmColor="#dc3545"
        iconName="warning-outline"
        iconColor="#ffc107"
        type="warning"
      />

      {/* Toast Notification */}
      <Toast
        visible={showToast}
        message={toastMessage}
        type={toastType}
        onHide={() => setShowToast(false)}
      />

      {/* Loading Overlay */}
      <LoadingOverlay
        visible={isAILoading}
        message="IA analisando o problema..."
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#dc3545',
    paddingHorizontal: 20,
    paddingVertical: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  backButton: {
    padding: 8,
    borderRadius: 6,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 16,
  },
  refreshButton: {
    padding: 8,
    borderRadius: 6,
  },
  listContainer: {
    padding: 20,
  },
  ticketCard: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  ticketHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  ticketInfo: {
    flex: 1,
  },
  ticketTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  ticketUser: {
    fontSize: 16,
    color: '#666',
    marginBottom: 2,
  },
  ticketDate: {
    fontSize: 14,
    color: '#999',
  },
  ticketDescription: {
    marginBottom: 15,
  },
  descriptionText: {
    fontSize: 16,
    color: '#666',
    lineHeight: 22,
  },
  ticketBadges: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 15,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  badgeIcon: {
    marginRight: 4,
  },
  badgeText: {
    color: '#fff',
    fontSize: 13,
    fontWeight: 'bold',
  },
  ticketActions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  actionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 6,
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  actionButtonText: {
    fontSize: 14,
    fontWeight: '600',
    marginLeft: 4,
    color: '#333',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
  },
  emptySubtitle: {
    fontSize: 18,
    color: '#666',
    textAlign: 'center',
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 12,
    width: '95%',
    maxHeight: '90%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
  },
  modalTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
  },
  modalBody: {
    maxHeight: 400,
    padding: 20,
  },
  ticketDetails: {
    marginBottom: 20,
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  detailTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  detailUser: {
    fontSize: 16,
    color: '#666',
    marginBottom: 10,
  },
  detailDescription: {
    fontSize: 16,
    color: '#666',
    lineHeight: 22,
  },
  aiSuggestion: {
    marginBottom: 20,
    padding: 15,
    backgroundColor: '#fff3cd',
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#ffc107',
  },
  aiHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  aiTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#856404',
    marginLeft: 8,
  },
  aiAnalysis: {
    fontSize: 16,
    color: '#856404',
    marginBottom: 10,
    fontStyle: 'italic',
  },
  aiStepsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#856404',
    marginBottom: 8,
  },
  aiStep: {
    fontSize: 15,
    color: '#856404',
    marginBottom: 4,
    paddingLeft: 10,
  },
  aiAdditional: {
    fontSize: 15,
    color: '#856404',
    marginTop: 8,
    fontStyle: 'italic',
  },
  aiText: {
    fontSize: 16,
    color: '#856404',
  },
  aiSection: {
    marginBottom: 12,
  },
  aiSectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#856404',
    marginBottom: 6,
  },
  aiLogStep: {
    fontSize: 12,
    color: '#6c757d',
    marginBottom: 3,
    marginLeft: 10,
    fontFamily: 'monospace',
    backgroundColor: '#f8f9fa',
    padding: 4,
    borderRadius: 4,
  },
  aiErrorStep: {
    fontSize: 12,
    color: '#dc3545',
    marginBottom: 3,
    marginLeft: 10,
    fontWeight: '500',
  },
  aiToolStep: {
    fontSize: 12,
    color: '#007bff',
    marginBottom: 3,
    marginLeft: 10,
    fontWeight: '500',
  },
  aiEscalation: {
    fontSize: 13,
    color: '#dc3545',
    fontWeight: '500',
    marginTop: 5,
    lineHeight: 18,
  },
  aiMetadata: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 15,
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: '#ffeaa7',
  },
  aiConfidence: {
    fontSize: 12,
    color: '#28a745',
    fontWeight: 'bold',
  },
  aiTime: {
    fontSize: 12,
    color: '#007bff',
    fontWeight: 'bold',
  },
  aiPriority: {
    fontSize: 12,
    color: '#dc3545',
    fontWeight: 'bold',
  },
  aiRootCause: {
    fontSize: 14,
    color: '#856404',
    fontWeight: '600',
    marginTop: 5,
    lineHeight: 20,
    backgroundColor: '#fff8e1',
    padding: 10,
    borderRadius: 6,
    borderLeftWidth: 3,
    borderLeftColor: '#ff9800',
  },
  aiStepNumber: {
    fontSize: 14,
    color: '#856404',
    marginBottom: 6,
    marginLeft: 10,
    lineHeight: 20,
    fontWeight: '500',
  },
  aiCommandStep: {
    fontSize: 12,
    color: '#007bff',
    marginBottom: 3,
    marginLeft: 10,
    fontFamily: 'monospace',
    backgroundColor: '#e3f2fd',
    padding: 6,
    borderRadius: 4,
    fontWeight: '500',
  },
  aiConfigStep: {
    fontSize: 12,
    color: '#6f42c1',
    marginBottom: 3,
    marginLeft: 10,
    fontFamily: 'monospace',
    backgroundColor: '#f3e5f5',
    padding: 4,
    borderRadius: 4,
    fontWeight: '500',
  },
  responseSection: {
    marginBottom: 20,
  },
  responseLabel: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  responseInput: {
    backgroundColor: '#f8f9fa',
    borderWidth: 2,
    borderColor: '#e9ecef',
    borderRadius: 8,
    paddingHorizontal: 15,
    paddingVertical: 12,
    fontSize: 18,
    color: '#333',
    minHeight: 100,
  },
  aiResponseOption: {
    marginBottom: 15,
  },
  aiToggleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 15,
    backgroundColor: '#fff3cd',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ffc107',
    marginBottom: 10,
  },
  aiToggleText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#856404',
    marginLeft: 10,
  },
  aiResponsePreview: {
    backgroundColor: '#d4edda',
    padding: 15,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#28a745',
  },
  aiResponseLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#155724',
    marginBottom: 8,
  },
  aiResponseText: {
    fontSize: 16,
    color: '#155724',
    lineHeight: 22,
  },
  aiLoading: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 15,
    backgroundColor: '#fff3cd',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ffc107',
  },
  aiLoadingText: {
    fontSize: 16,
    color: '#856404',
    marginLeft: 10,
    fontStyle: 'italic',
  },
  modalFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
    gap: 15,
  },
  cancelButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#6c757d',
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  finalizeButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 20,
    borderRadius: 8,
    backgroundColor: '#dc3545',
    alignItems: 'center',
  },
  finalizeButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
});

export default PendingTicketsScreen;
