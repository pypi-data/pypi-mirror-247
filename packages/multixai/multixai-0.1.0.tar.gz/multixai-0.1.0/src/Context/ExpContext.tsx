/* eslint-disable react-refresh/only-export-components */

import React, { createContext, useState, Dispatch, SetStateAction, ReactNode, useContext } from 'react';
import {AllExplanations} from 'src/Types/types'

import * as _initialState from 'src/asset/vis_data_test.json'

const initialState = _initialState as AllExplanations;

export const ExpContext = createContext({
    exp: {} as AllExplanations,
    setExp: {} as Dispatch<SetStateAction<AllExplanations>>
});

interface ExpProviderProps {
  children: ReactNode;
  value?: Partial<AllExplanations>;
}


export const ExpProvider = ( {children, value = initialState}: ExpProviderProps ) => {
  const [exp, setExp] = useState({...initialState, ...value});
  
  return <ExpContext.Provider value={{ exp, setExp}}>
      {children}
    </ExpContext.Provider>
};


export const useExp = () => {
  const context = useContext(ExpContext);
  if (!context) {
    throw new Error('useExp must be used within a ExpContextProvider');
  }
  return context;
};