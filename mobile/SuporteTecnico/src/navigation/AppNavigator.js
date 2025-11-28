import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import HomeScreen from '../screens/HomeScreen';
import LoginScreen from '../screens/LoginScreen';
import TicketDetailScreen from '../screens/TicketDetailScreen';
import CreateTicketScreen from '../screens/CreateTicketScreen';
import PendingTicketsScreen from '../screens/PendingTicketsScreen';
import CompletedTicketsScreen from '../screens/CompletedTicketsScreen';
import SettingsScreen from '../screens/SettingsScreen';
import { TicketProvider } from '../context/TicketContext';

const Stack = createStackNavigator();

const AppNavigator = () => {
  console.log('AppNavigator: Renderizando...');
  
  return (
    <TicketProvider>
      <NavigationContainer>
        <Stack.Navigator 
          initialRouteName="Login"
          screenOptions={{
            headerStyle: {
              backgroundColor: '#dc3545',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen 
            name="Login" 
            component={LoginScreen} 
            options={{ title: 'Login' }}
          />
          <Stack.Screen 
            name="Home" 
            component={HomeScreen} 
            options={{ title: 'Suporte Técnico' }}
          />
          <Stack.Screen 
            name="TicketDetail" 
            component={TicketDetailScreen} 
            options={{ title: 'Detalhes do Ticket' }}
          />
          <Stack.Screen 
            name="CreateTicket" 
            component={CreateTicketScreen} 
            options={{ title: 'Abrir Chamado' }}
          />
          <Stack.Screen 
            name="PendingTickets" 
            component={PendingTicketsScreen} 
            options={{ title: 'Chamados em Andamento' }}
          />
              <Stack.Screen 
                name="CompletedTickets" 
                component={CompletedTicketsScreen} 
                options={{ title: 'Chamados Finalizados' }}
              />
              <Stack.Screen 
                name="Settings" 
                component={SettingsScreen} 
                options={{ title: 'Configurações' }}
              />
        </Stack.Navigator>
      </NavigationContainer>
    </TicketProvider>
  );
};

export default AppNavigator;
