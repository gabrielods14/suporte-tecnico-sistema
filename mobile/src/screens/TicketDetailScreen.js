import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { api } from '../services/api';

const TicketDetailScreen = ({ route, navigation }) => {
  const { ticketId } = route.params;
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sendingMessage, setSendingMessage] = useState(false);
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    fetchTicket();
  }, [ticketId]);

  const fetchTicket = async () => {
    try {
      const data = await api.getTicket(ticketId);
      setTicket(data);
    } catch (error) {
      Alert.alert('Erro', 'Erro ao carregar detalhes do chamado');
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim()) {
      Alert.alert('Erro', 'Por favor, digite uma mensagem');
      return;
    }

    if (ticket.status !== 'Aberto') {
      Alert.alert('Erro', 'Este chamado estÃ¡ fechado e nÃ£o aceita novas mensagens');
      return;
    }

    setSendingMessage(true);
    try {
      const result = await api.addMessage(ticketId, newMessage.trim());
      if (result.success) {
        setNewMessage('');
        // Atualizar o ticket localmente
        setTicket(prevTicket => ({
          ...prevTicket,
          messages: [...prevTicket.messages, result.message],
          updatedAt: result.message.timestamp
        }));
        Alert.alert('Sucesso', 'Mensagem enviada com sucesso!');
      } else {
        Alert.alert('Erro', result.error || 'Erro ao enviar mensagem');
      }
    } catch (error) {
      Alert.alert('Erro', 'Erro ao enviar mensagem');
    } finally {
      setSendingMessage(false);
    }
  };

  const formatDateTime = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Aberto':
        return '#4CAF50';
      case 'Fechado':
        return '#757575';
      default:
        return '#FF9800';
    }
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Alta':
        return '#F44336';
      case 'MÃ©dia':
        return '#FF9800';
      case 'Baixa':
        return '#4CAF50';
      default:
        return '#757575';
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2E7D32" />
        <Text style={styles.loadingText}>Carregando detalhes...</Text>
      </View>
    );
  }

  if (!ticket) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>Chamado nÃ£o encontrado</Text>
      </View>
    );
  }

  const canReply = ticket.status === 'Aberto';

  return (
    <KeyboardAvoidingView 
      style={styles.container} 
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* InformaÃ§Ãµes do chamado */}
        <View style={styles.ticketInfo}>
          <Text style={styles.ticketTitle}>{ticket.title}</Text>
          
          <View style={styles.statusContainer}>
            <View style={[styles.statusBadge, { backgroundColor: getStatusColor(ticket.status) }]}>
              <Text style={styles.statusText}>{ticket.status}</Text>
            </View>
            <View style={[styles.priorityBadge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
              <Text style={styles.priorityText}>{ticket.priority}</Text>
            </View>
          </View>

          <Text style={styles.ticketDescription}>{ticket.description}</Text>
          
          <View style={styles.ticketMeta}>
            <Text style={styles.metaText}>Chamado #{ticket.id}</Text>
            <Text style={styles.metaText}>Criado em: {formatDateTime(ticket.createdAt)}</Text>
            <Text style={styles.metaText}>Atualizado em: {formatDateTime(ticket.updatedAt)}</Text>
          </View>
        </View>

        {/* HistÃ³rico de mensagens */}
        <View style={styles.messagesContainer}>
          <Text style={styles.sectionTitle}>HistÃ³rico de Mensagens</Text>
          
          {ticket.messages.map((message, index) => (
            <View key={message.id} style={styles.messageContainer}>
              <View style={[
                styles.messageBubble,
                message.sender === 'user' ? styles.userMessage : styles.supportMessage
              ]}>
                <Text style={[
                  styles.messageText,
                  message.sender === 'user' ? styles.userMessageText : styles.supportMessageText
                ]}>
                  {message.text}
                </Text>
                <Text style={[
                  styles.messageTime,
                  message.sender === 'user' ? styles.userMessageTime : styles.supportMessageTime
                ]}>
                  {formatDateTime(message.timestamp)}
                </Text>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>

      {/* Campo de resposta (apenas para chamados abertos) */}
      {canReply && (
        <View style={styles.replyContainer}>
          <View style={styles.replyInputContainer}>
            <TextInput
              style={styles.replyInput}
              value={newMessage}
              onChangeText={setNewMessage}
              placeholder="Digite sua resposta..."
              multiline
              maxLength={500}
            />
            <Text style={styles.characterCount}>
              {newMessage.length}/500
            </Text>
          </View>
          
          <TouchableOpacity
            style={[styles.sendButton, sendingMessage && styles.sendButtonDisabled]}
            onPress={handleSendMessage}
            disabled={sendingMessage}
          >
            {sendingMessage ? (
              <ActivityIndicator color="#fff" size="small" />
            ) : (
              <Text style={styles.sendButtonText}>Enviar</Text>
            )}
          </TouchableOpacity>
        </View>
      )}

      {/* Aviso para chamados fechados */}
      {!canReply && (
        <View style={styles.closedNotice}>
          <Text style={styles.closedNoticeText}>
            Este chamado estÃ¡ fechado e nÃ£o aceita novas mensagens
          </Text>
        </View>
      )}
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  errorText: {
    fontSize: 18,
    color: '#666',
  },
  scrollView: {
    flex: 1,
  },
  ticketInfo: {
    backgroundColor: '#fff',
    margin: 16,
    padding: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  ticketTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: '#333',
    marginBottom: 12,
  },
  statusContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    marginRight: 8,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  priorityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  priorityText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  ticketDescription: {
    fontSize: 16,
    color: '#666',
    lineHeight: 24,
    marginBottom: 16,
  },
  ticketMeta: {
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    paddingTop: 12,
  },
  metaText: {
    fontSize: 12,
    color: '#999',
    marginBottom: 4,
  },
  messagesContainer: {
    margin: 16,
    marginTop: 0,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  messageContainer: {
    marginBottom: 12,
  },
  messageBubble: {
    padding: 12,
    borderRadius: 12,
    maxWidth: '80%',
  },
  userMessage: {
    backgroundColor: '#2E7D32',
    alignSelf: 'flex-end',
  },
  supportMessage: {
    backgroundColor: '#fff',
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderColor: '#e0e0e0',
  },
  messageText: {
    fontSize: 14,
    lineHeight: 20,
  },
  userMessageText: {
    color: '#fff',
  },
  supportMessageText: {
    color: '#333',
  },
  messageTime: {
    fontSize: 10,
    marginTop: 4,
  },
  userMessageTime: {
    color: '#e8f5e8',
  },
  supportMessageTime: {
    color: '#999',
  },
  replyContainer: {
    backgroundColor: '#fff',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  replyInputContainer: {
    marginBottom: 12,
  },
  replyInput: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 14,
    minHeight: 80,
    textAlignVertical: 'top',
  },
  characterCount: {
    fontSize: 10,
    color: '#999',
    textAlign: 'right',
    marginTop: 4,
  },
  sendButton: {
    backgroundColor: '#2E7D32',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  sendButtonDisabled: {
    backgroundColor: '#a5d6a7',
  },
  sendButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  closedNotice: {
    backgroundColor: '#f5f5f5',
    padding: 16,
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  closedNoticeText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
});

export default TicketDetailScreen;
