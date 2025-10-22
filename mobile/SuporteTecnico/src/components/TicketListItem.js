import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';

const TicketListItem = ({ ticket, onPress }) => {
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
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <Text style={styles.title}>{ticket.title}</Text>
          <Text style={styles.date}>{ticket.date}</Text>
        </View>
        <Icon name="chevron-forward" size={20} color="#666" />
      </View>
      
      <View style={styles.badges}>
        <View style={[styles.badge, { backgroundColor: getPriorityColor(ticket.priority) }]}>
          <Text style={styles.badgeText}>{ticket.priority}</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: getStatusColor(ticket.status) }]}>
          <Icon name={getStatusIcon(ticket.status)} size={12} color="#fff" style={styles.badgeIcon} />
          <Text style={styles.badgeText}>{ticket.status}</Text>
        </View>
      </View>
      
      <View style={styles.footer}>
        <Text style={styles.id}>ID: {ticket.id}</Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    padding: 20,
    marginBottom: 15,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
    borderLeftWidth: 4,
    borderLeftColor: '#dc3545',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  titleContainer: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
    lineHeight: 20,
  },
  date: {
    fontSize: 12,
    color: '#666',
    fontWeight: '500',
  },
  badges: {
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
  footer: {
    borderTopWidth: 1,
    borderTopColor: '#f0f0f0',
    paddingTop: 10,
  },
  id: {
    fontSize: 11,
    color: '#999',
    fontWeight: '500',
  },
});

export default TicketListItem;
