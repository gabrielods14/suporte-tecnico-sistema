import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';

import HomeScreen from '../screens/HomeScreen';
import LoginScreen from '../screens/LoginScreen';
import TicketDetailScreen from '../screens/TicketDetailScreen';
import CreateTicketScreen from '../screens/CreateTicketScreen';
import PendingTicketsScreen from '../screens/PendingTicketsScreen';
import CompletedTicketsScreen from '../screens/CompletedTicketsScreen';
import { TicketProvider } from '../context/TicketContext';

const Stack = createStackNavigator();

const AppNavigator = () => {
  return (
    <TicketProvider>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login">
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
        </Stack.Navigator>
      </NavigationContainer>
    </TicketProvider>
  );
};

export default AppNavigator;
