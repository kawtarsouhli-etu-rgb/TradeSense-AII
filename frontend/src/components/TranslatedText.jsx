// src/components/TranslatedText.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

const TranslatedText = ({ children, ns, keyName, defaultValue, ...props }) => {
  const { t } = useTranslation(ns);
  
  // If keyName is provided, use it as the translation key
  // Otherwise, use children as the key
  const translationKey = keyName || children;
  
  // Get translation, falling back to defaultValue or children if not found
  const translatedText = t(translationKey, defaultValue || children);
  
  return <span {...props}>{translatedText}</span>;
};

export default TranslatedText;