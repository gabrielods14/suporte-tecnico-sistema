import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import { useTickets } from '../context/TicketContext';

const CompletedTicketsScreen = ({ navigation }) => {
  const { getTicketsByStatus } = useTickets();
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = () => {
    const completedTickets = getTicketsByStatus('Fechado');
    setTickets(completedTickets);
  };

  const getPriorityColor = (priority) => {
    switch (priority) {
      case 'Alta': return '#dc3545';
      case 'Média': return '#ffc107';
      case 'Baixa': return '#28a745';
      default: return '#6c757d';
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

  const renderTicketItem = ({ item: ticket }) => (
    <TouchableOpacity style={styles.ticketCard}>
      <View style={styles.ticketHeader}>
        <View style={styles.ticketInfo}>
          <Text style={styles.ticketTitle}>{ticket.title}</Text>
          <Text style={styles.ticketUser}>Por: {ticket.user}</Text>
          <Text style={styles.ticketDate}>Criado: {ticket.createdAt}</Text>
          <Text style={styles.completedDate}>Finalizado: {ticket.completedAt}</Text>
          {ticket.completedBy && (
            <Text style={styles.technicianInfo}>Finalizado por: {ticket.completedBy}</Text>
          )}
          {ticket.lastRespondedBy && (
            <Text style={styles.lastResponseInfo}>Última resposta: {ticket.lastRespondedBy}</Text>
          )}
        </View>
        <Icon name="checkmark-circle" size={24} color="#28a745" />
      </View>

      <View style={styles.ticketDescription}>
        <Text style={styles.descriptionText} numberOfLines={3}>
          {ticket.description}
        </Text>
      </View>

      <View style={styles.ticketBadges}>
        <View style={[styles.badge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
          <Text style={styles.badgeText}>{ticket.priority}</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: '#28a745' }]}>
          <Icon name="checkmark-circle-outline" size={12} color="#fff" style={styles.badgeIcon} />
          <Text style={styles.badgeText}>Finalizado</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: '#6c757d' }]}>
          <Icon name={getProblemTypeIcon(ticket.type)} size={12} color="#fff" style={styles.badgeIcon} />
          <Text style={styles.badgeText}>{ticket.type}</Text>
        </View>
      </View>

      {ticket.responses && ticket.responses.length > 0 && (
        <View style={styles.responsesSection}>
          <Text style={styles.responsesTitle}>Respostas do Técnico:</Text>
          {ticket.responses.map((response, index) => (
            <View key={index} style={styles.responseItem}>
              <Text style={styles.responseText}>{response.text}</Text>
              <Text style={styles.responseMeta}>
                {response.technician} - {response.timestamp}
              </Text>
            </View>
          ))}
        </View>
      )}
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
        <Text style={styles.headerTitle}>Chamados Finalizados</Text>
        <TouchableOpacity 
          style={styles.refreshButton}
          onPress={loadTickets}
        >
          <Icon name="refresh-outline" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      {/* Stats */}
      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Icon name="checkmark-circle" size={32} color="#28a745" />
          <Text style={styles.statNumber}>{tickets.length}</Text>
          <Text style={styles.statLabel}>Chamados Finalizados</Text>
        </View>
        
        {tickets.length > 0 && (
          <View style={styles.technicianStats}>
            <Text style={styles.statsTitle}>Técnicos que Finalizaram:</Text>
            {(() => {
              const technicians = [...new Set(tickets.map(ticket => ticket.completedBy).filter(Boolean))];
              return technicians.map((technician, index) => {
                const count = tickets.filter(ticket => ticket.completedBy === technician).length;
                return (
                  <View key={index} style={styles.technicianItem}>
                    <Icon name="person-circle-outline" size={16} color="#dc3545" />
                    <Text style={styles.technicianName}>{technician}</Text>
                    <Text style={styles.technicianCount}>({count})</Text>
                  </View>
                );
              });
            })()}
          </View>
        )}
      </View>

      {/* Tickets List */}
      <FlatList
        data={tickets}
        keyExtractor={(item) => item.id}
        renderItem={renderTicketItem}
        contentContainerStyle={styles.listContainer}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Icon name="folder-open-outline" size={64} color="#6c757d" />
            <Text style={styles.emptyTitle}>Nenhum chamado finalizado</Text>
            <Text style={styles.emptySubtitle}>
              Os chamados finalizados aparecerão aqui
            </Text>
          </View>
        }
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
    fontSize: 18,
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
  statsContainer: {
    backgroundColor: '#fff',
    padding: 20,
    margin: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#28a745',
    marginTop: 8,
  },
  statLabel: {
    fontSize: 14,
    color: '#666',
    marginTop: 4,
  },
  technicianStats: {
    marginTop: 20,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  statsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  technicianItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  technicianName: {
    fontSize: 14,
    color: '#333',
    marginLeft: 8,
    flex: 1,
  },
  technicianCount: {
    fontSize: 14,
    color: '#dc3545',
    fontWeight: 'bold',
  },
  listContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
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
    borderLeftWidth: 4,
    borderLeftColor: '#28a745',
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
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  ticketUser: {
    fontSize: 14,
    color: '#666',
    marginBottom: 2,
  },
  ticketDate: {
    fontSize: 12,
    color: '#999',
    marginBottom: 2,
  },
  completedDate: {
    fontSize: 12,
    color: '#28a745',
    fontWeight: '600',
  },
  technicianInfo: {
    fontSize: 12,
    color: '#dc3545',
    fontWeight: '600',
    marginTop: 2,
  },
  lastResponseInfo: {
    fontSize: 12,
    color: '#007bff',
    fontWeight: '500',
    marginTop: 2,
  },
  ticketDescription: {
    marginBottom: 15,
  },
  descriptionText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
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
    fontSize: 11,
    fontWeight: 'bold',
  },
  responsesSection: {
    marginTop: 15,
    paddingTop: 15,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  responsesTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  responseItem: {
    backgroundColor: '#f8f9fa',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  responseText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
    marginBottom: 5,
  },
  responseMeta: {
    fontSize: 12,
    color: '#666',
    fontStyle: 'italic',
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 20,
    marginBottom: 10,
  },
  emptySubtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
});

export default CompletedTicketsScreen;
