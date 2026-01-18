// src/components/LanguageSwitcher.jsx
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './LanguageSwitcher.css';

const LanguageSwitcher = () => {
  const { i18n, t } = useTranslation();
  const [isOpen, setIsOpen] = useState(false);

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    // Update direction for RTL languages
    document.documentElement.dir = lng === 'ar' ? 'rtl' : 'ltr';
    setIsOpen(false); // Close the dropdown after selection
  };

  const getCurrentLanguageName = () => {
    switch (i18n.language) {
      case 'fr': return 'Français';
      case 'ar': return 'العربية';
      default: return 'English';
    }
  };

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  // Close dropdown when clicking outside
  React.useEffect(() => {
    const handleClickOutside = (event) => {
      const switcherElement = document.querySelector('.language-switcher');
      if (switcherElement && !switcherElement.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className={`language-switcher ${isOpen ? 'show' : ''}`}>
      <div className="dropdown">
        <button 
          className="dropdown-toggle" 
          type="button" 
          id="languageDropdown"
          onClick={toggleDropdown}
          aria-haspopup="true"
          aria-expanded={isOpen}
        >
          <span className="language-flag">{getCurrentLanguageName()}</span>
          <span className={`language-arrow ${isOpen ? 'rotated' : ''}`}>▼</span>
        </button>
        {isOpen && (
          <ul className="dropdown-menu" aria-labelledby="languageDropdown">
            <li>
              <button 
                className={`dropdown-item ${i18n.language === 'en' ? 'active' : ''}`}
                onClick={() => changeLanguage('en')}
              >
                🇺🇸 English
              </button>
            </li>
            <li>
              <button 
                className={`dropdown-item ${i18n.language === 'fr' ? 'active' : ''}`}
                onClick={() => changeLanguage('fr')}
              >
                🇫🇷 Français
              </button>
            </li>
            <li>
              <button 
                className={`dropdown-item ${i18n.language === 'ar' ? 'active' : ''}`}
                onClick={() => changeLanguage('ar')}
              >
                🇸🇦 العربية
              </button>
            </li>
          </ul>
        )}
      </div>
    </div>
  );
};

export default LanguageSwitcher;