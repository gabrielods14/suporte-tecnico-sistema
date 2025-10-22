import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import ConfirmationModal from '../components/ConfirmationModal';

const TicketDetailScreen = ({ route, navigation }) => {
  const { ticket } = route.params;
  const [showBackModal, setShowBackModal] = useState(false);

  const handleBackPress = () => {
    setShowBackModal(true);
  };

  const confirmBack = () => {
    setShowBackModal(false);
    navigation.goBack();
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Alta':
        return '#dc3545';
      case 'Média':
        return '#fd7e14';
      case 'Baixa':
        return '#28a745';
      default:
        return '#6c757d';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'Aberto':
        return '#dc3545';
      case 'Em andamento':
        return '#fd7e14';
      case 'Fechado':
        return '#28a745';
      default:
        return '#6c757d';
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'Aberto':
        return 'alert-circle-outline';
      case 'Em andamento':
        return 'time-outline';
      case 'Fechado':
        return 'checkmark-circle-outline';
      default:
        return 'help-circle-outline';
    }
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#dc3545" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton} 
          onPress={handleBackPress}
        >
          <Icon name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Detalhes do Ticket</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Ticket Header */}
        <View style={styles.ticketHeader}>
          <Text style={styles.ticketTitle}>{ticket.title}</Text>
          <View style={styles.badges}>
            <View style={[styles.badge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
              <Text style={styles.badgeText}>{ticket.priority}</Text>
            </View>
            <View style={[styles.badge, { backgroundColor: getStatusColor(ticket.status) }]}>
              <Icon name={getStatusIcon(ticket.status)} size={14} color="#fff" style={styles.badgeIcon} />
              <Text style={styles.badgeText}>{ticket.status}</Text>
            </View>
          </View>
        </View>

        {/* Ticket Info */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Icon name="information-circle-outline" size={20} color="#dc3545" />
            <Text style={styles.sectionTitle}>Informações do Ticket</Text>
          </View>
          
          <View style={styles.infoGrid}>
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>ID do Ticket</Text>
              <Text style={styles.infoValue}>#{ticket.id}</Text>
            </View>
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>Data de Criação</Text>
              <Text style={styles.infoValue}>{ticket.date}</Text>
            </View>
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>Prioridade</Text>
              <View style={[styles.priorityBadge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
                <Text style={styles.priorityText}>{ticket.priority}</Text>
              </View>
            </View>
            <View style={styles.infoItem}>
              <Text style={styles.infoLabel}>Status Atual</Text>
              <View style={[styles.statusBadge, { backgroundColor: getStatusColor(ticket.status) }]}>
                <Icon name={getStatusIcon(ticket.status)} size={14} color="#fff" />
                <Text style={styles.statusText}>{ticket.status}</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Description */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Icon name="document-text-outline" size={20} color="#dc3545" />
            <Text style={styles.sectionTitle}>Descrição do Problema</Text>
          </View>
          <Text style={styles.description}>
            Este é um exemplo de descrição do ticket. Aqui seria exibida a descrição completa
            do problema reportado pelo usuário, incluindo detalhes técnicos e informações
            relevantes para a resolução do chamado de suporte técnico.
          </Text>
        </View>

        {/* Actions */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Icon name="construct-outline" size={20} color="#dc3545" />
            <Text style={styles.sectionTitle}>Ações Disponíveis</Text>
          </View>
          
          <TouchableOpacity style={styles.primaryActionButton}>
            <Icon name="refresh-outline" size={20} color="#fff" />
            <Text style={styles.primaryActionText}>Atualizar Status</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.secondaryActionButton}>
            <Icon name="chatbubble-outline" size={20} color="#dc3545" />
            <Text style={styles.secondaryActionText}>Adicionar Comentário</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.secondaryActionButton}>
            <Icon name="attach-outline" size={20} color="#dc3545" />
            <Text style={styles.secondaryActionText}>Anexar Arquivo</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      {/* Back Confirmation Modal */}
      <ConfirmationModal
        visible={showBackModal}
        onClose={() => setShowBackModal(false)}
        onConfirm={confirmBack}
        title="Voltar"
        message="Tem certeza que deseja voltar? Você perderá a visualização atual do ticket."
        confirmText="Voltar"
        cancelText="Continuar Visualizando"
        confirmColor="#6c757d"
        iconName="arrow-back-outline"
        iconColor="#6c757d"
        type="info"
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
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  backButton: {
    padding: 8,
    borderRadius: 6,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#fff',
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 16,
  },
  headerSpacer: {
    width: 40,
  },
  content: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 20,
  },
  ticketHeader: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  ticketTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    lineHeight: 26,
  },
  badges: {
    flexDirection: 'row',
    gap: 12,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 20,
  },
  badgeIcon: {
    marginRight: 6,
  },
  badgeText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 12,
  },
  section: {
    backgroundColor: '#fff',
    padding: 20,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 10,
  },
  infoGrid: {
    gap: 15,
  },
  infoItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  infoLabel: {
    fontSize: 14,
    color: '#666',
    fontWeight: '500',
    flex: 1,
  },
  infoValue: {
    fontSize: 14,
    color: '#333',
    fontWeight: 'bold',
  },
  priorityBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  priorityText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: 'bold',
    marginLeft: 6,
  },
  description: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  primaryActionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc3545',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 12,
    shadowColor: '#dc3545',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  primaryActionText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
    marginLeft: 8,
  },
  secondaryActionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#dc3545',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 8,
    marginBottom: 12,
  },
  secondaryActionText: {
    color: '#dc3545',
    fontWeight: 'bold',
    fontSize: 16,
    marginLeft: 8,
  },
});

export default TicketDetailScreen;
