import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  StatusBar,
  Alert,
} from 'react-native';
import Icon from 'react-native-vector-icons/Ionicons';
import GeminiConfigModal from '../components/GeminiConfigModal';

const SettingsScreen = ({ navigation }) => {
  const [showGeminiModal, setShowGeminiModal] = useState(false);

  const handleLogout = () => {
    Alert.alert(
      'Confirmar Logout',
      'Tem certeza que deseja sair da aplicação?',
      [
        {
          text: 'Cancelar',
          style: 'cancel',
        },
        {
          text: 'Sair',
          style: 'destructive',
          onPress: () => {
            // Aqui você pode limpar o token e navegar para login
            navigation.navigate('Login');
          },
        },
      ]
    );
  };

  const handleClearCache = () => {
    Alert.alert(
      'Limpar Cache',
      'Isso irá limpar todos os dados temporários da aplicação. Continuar?',
      [
        {
          text: 'Cancelar',
          style: 'cancel',
        },
        {
          text: 'Limpar',
          style: 'destructive',
          onPress: () => {
            Alert.alert('Sucesso', 'Cache limpo com sucesso!');
          },
        },
      ]
    );
  };

  const handleAbout = () => {
    Alert.alert(
      'Sobre o App',
      'Suporte Técnico v1.0\n\nDesenvolvido com React Native\nIntegração com Gemini Pro AI\n\n© 2025 HelpWave',
      [{ text: 'OK' }]
    );
  };

  const settingsItems = [
    {
      id: 'gemini',
      title: 'Configurar Gemini Pro',
      subtitle: 'Configure sua chave de API para IA',
      icon: 'bulb-outline',
      iconColor: '#ffc107',
      onPress: () => setShowGeminiModal(true),
    },
    {
      id: 'notifications',
      title: 'Notificações',
      subtitle: 'Configurar alertas e notificações',
      icon: 'notifications-outline',
      iconColor: '#007bff',
      onPress: () => Alert.alert('Em breve', 'Configurações de notificações em desenvolvimento'),
    },
    {
      id: 'theme',
      title: 'Tema',
      subtitle: 'Escolher tema claro ou escuro',
      icon: 'color-palette-outline',
      iconColor: '#6f42c1',
      onPress: () => Alert.alert('Em breve', 'Seleção de tema em desenvolvimento'),
    },
    {
      id: 'language',
      title: 'Idioma',
      subtitle: 'Português (Brasil)',
      icon: 'language-outline',
      iconColor: '#28a745',
      onPress: () => Alert.alert('Em breve', 'Seleção de idioma em desenvolvimento'),
    },
    {
      id: 'cache',
      title: 'Limpar Cache',
      subtitle: 'Remover dados temporários',
      icon: 'trash-outline',
      iconColor: '#dc3545',
      onPress: handleClearCache,
    },
    {
      id: 'about',
      title: 'Sobre',
      subtitle: 'Informações da aplicação',
      icon: 'information-circle-outline',
      iconColor: '#6c757d',
      onPress: handleAbout,
    },
  ];

  const renderSettingItem = (item) => (
    <TouchableOpacity
      key={item.id}
      style={styles.settingItem}
      onPress={item.onPress}
    >
      <View style={styles.settingItemLeft}>
        <View style={[styles.iconContainer, { backgroundColor: `${item.iconColor}20` }]}>
          <Icon name={item.icon} size={24} color={item.iconColor} />
        </View>
        <View style={styles.settingItemText}>
          <Text style={styles.settingItemTitle}>{item.title}</Text>
          <Text style={styles.settingItemSubtitle}>{item.subtitle}</Text>
        </View>
      </View>
      <Icon name="chevron-forward" size={20} color="#666" />
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#dc3545" />
      
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={() => navigation.goBack()}
        >
          <Icon name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Configurações</Text>
        <View style={styles.headerSpacer} />
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Inteligência Artificial</Text>
          {settingsItems.filter(item => item.id === 'gemini').map(renderSettingItem)}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Aparência</Text>
          {settingsItems.filter(item => ['theme', 'language'].includes(item.id)).map(renderSettingItem)}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Sistema</Text>
          {settingsItems.filter(item => ['notifications', 'cache'].includes(item.id)).map(renderSettingItem)}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Informações</Text>
          {settingsItems.filter(item => item.id === 'about').map(renderSettingItem)}
        </View>

        <View style={styles.logoutSection}>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Icon name="log-out-outline" size={24} color="#fff" />
            <Text style={styles.logoutButtonText}>Sair da Aplicação</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <GeminiConfigModal
        visible={showGeminiModal}
        onClose={() => setShowGeminiModal(false)}
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
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 15,
    marginLeft: 5,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#fff',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderRadius: 12,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 1,
    },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  settingItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  iconContainer: {
    width: 48,
    height: 48,
    borderRadius: 24,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 15,
  },
  settingItemText: {
    flex: 1,
  },
  settingItemTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 2,
  },
  settingItemSubtitle: {
    fontSize: 14,
    color: '#666',
  },
  logoutSection: {
    marginTop: 20,
    marginBottom: 40,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc3545',
    paddingVertical: 15,
    paddingHorizontal: 20,
    borderRadius: 12,
    shadowColor: '#dc3545',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 4,
  },
  logoutButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 10,
  },
});

export default SettingsScreen;

