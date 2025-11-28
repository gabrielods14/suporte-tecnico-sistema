import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  ScrollView,
  StatusBar,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import ConfirmationModal from '../components/ConfirmationModal';

const HomeScreen = ({ navigation }) => {
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  const handleLogout = () => {
    setShowLogoutModal(true);
  };

  const confirmLogout = () => {
    setShowLogoutModal(false);
    navigation.navigate('Login');
  };

  const dashboardCards = [
    {
      id: '1',
      title: 'NOVO CHAMADO',
      icon: 'create-outline',
      color: '#dc3545',
      onPress: () => navigation.navigate('CreateTicket'),
    },
    {
      id: '2',
      title: 'CHAMADOS EM ANDAMENTO',
      icon: 'list-outline',
      color: '#dc3545',
      onPress: () => navigation.navigate('PendingTickets'),
    },
    {
      id: '3',
      title: 'CHAMADOS CONCLUÍDOS',
      icon: 'checkmark-circle-outline',
      color: '#dc3545',
      onPress: () => navigation.navigate('CompletedTickets'),
    },
  ];

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#dc3545" />
      
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>HelpWave</Text>
        <View style={styles.headerButtons}>
          <TouchableOpacity 
            style={styles.settingsButton} 
            onPress={() => navigation.navigate('Settings')}
          >
            <Icon name="settings-outline" size={24} color="#fff" />
          </TouchableOpacity>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Icon name="log-out-outline" size={24} color="#fff" />
          </TouchableOpacity>
        </View>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Welcome Section */}
        <View style={styles.welcomeSection}>
          <Text style={styles.welcomeText}>BEM VINDO (A)</Text>
        </View>

        {/* Dashboard Cards */}
        <View style={styles.cardsContainer}>
          <View style={styles.cardsRow}>
            {dashboardCards.map((card) => (
              <TouchableOpacity key={card.id} style={styles.card} onPress={card.onPress}>
                <Icon name={card.icon} size={40} color="#fff" style={styles.cardIcon} />
                <Text style={styles.cardText}>{card.title}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Footer */}
        <View style={styles.footer}>
          <Text style={styles.footerText}>HelpWave — Simplificando o seu suporte.</Text>
          <Text style={styles.footerCopyright}>© 2025 HelpWave</Text>
        </View>
      </ScrollView>

      {/* Logout Confirmation Modal */}
      <ConfirmationModal
        visible={showLogoutModal}
        onClose={() => setShowLogoutModal(false)}
        onConfirm={confirmLogout}
        title="Confirmar Logout"
        message="Tem certeza que deseja sair do sistema? Você precisará fazer login novamente para acessar o aplicativo."
        confirmText="Sair"
        cancelText="Cancelar"
        confirmColor="#dc3545"
        iconName="log-out-outline"
        iconColor="#dc3545"
        type="warning"
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
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: '#dc3545',
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    letterSpacing: 1,
  },
  headerButtons: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  settingsButton: {
    padding: 8,
    borderRadius: 6,
    marginRight: 10,
  },
  logoutButton: {
    padding: 8,
    borderRadius: 6,
  },
  content: {
    flex: 1,
  },
  welcomeSection: {
    paddingHorizontal: 30,
    paddingVertical: 30,
    alignItems: 'center',
  },
  welcomeText: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#333',
    letterSpacing: 2,
  },
  cardsContainer: {
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  cardsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  card: {
    backgroundColor: '#8B0000',
    width: '48%',
    padding: 20,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 15,
    minHeight: 120,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 3.84,
    elevation: 5,
  },
  cardIcon: {
    marginBottom: 10,
  },
  cardText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    textAlign: 'center',
    letterSpacing: 0.5,
  },
  footer: {
    paddingHorizontal: 30,
    paddingVertical: 30,
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
    marginTop: 20,
  },
  footerText: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 5,
  },
  footerCopyright: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
  },
});

export default HomeScreen;
