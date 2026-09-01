const ComponentFunction = function() {
  // @section:imports @depends:[]
  const React = require('react');
  const { useState, useEffect, useContext, useMemo, useCallback } = React;
  const { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput, Modal, Alert, Platform, StatusBar, ActivityIndicator, KeyboardAvoidingView, FlatList, Dimensions, Image } = require('react-native');
  const { Ionicons } = require('@react-native-vector-icons/ionicons');
  const { MaterialIcons } = require('@react-native-vector-icons/material-icons');
  const { createBottomTabNavigator } = require('@react-navigation/bottom-tabs');
  const { createStackNavigator } = require('@react-navigation/stack');
  const { useSafeAreaInsets } = require('react-native-safe-area-context');
  const { useQuery, useMutation, useStorage } = require('platform-hooks');
  // @end:imports

  // @section:theme @depends:[]
  var TAB_MENU_HEIGHT = Platform.OS === 'web' ? 56 : 49;
  var SCROLL_EXTRA_PADDING = 16;
  var WEB_TAB_MENU_PADDING = 90;
  var FAB_SPACING = 16;

  const storageStrategy = 'all-local';
  const primaryColor = '#FF1493';
  const accentColor = '#FF6B35';
  const backgroundColor = '#F8F4FF';
  const cardColor = '#FFFFFF';
  const textPrimary = '#1A1A1A';
  const textSecondary = '#666666';
  const designStyle = 'modern';

  const WHATSAPP_NUMBER = '201006328846';
  // @end:theme

  // @section:constants @depends:[]
  var CATEGORIES = [
    { id: 'business_cards', name: 'Business Cards', name_ar: 'كروت شخصية' },
    { id: 'flyers', name: 'Flyers', name_ar: 'فلايرز' },
    { id: 'brochures', name: 'Brochures', name_ar: 'بروشورات' },
    { id: 'posters', name: 'Posters', name_ar: 'بوسترات' },
    { id: 'envelopes', name: 'Envelopes', name_ar: 'مظاريف' },
    { id: 'stickers', name: 'Stickers', name_ar: 'ستيكرز' },
    { id: 'notebooks', name: 'Notebooks', name_ar: 'دفاتر' },
    { id: 'block_notes', name: 'Block Notes', name_ar: 'بلوك نوت' },
    { id: 'menus', name: 'Menus', name_ar: 'منيوهات' },
    { id: 'books', name: 'Books', name_ar: 'كتب' },
    { id: 'packaging', name: 'Packaging', name_ar: 'تغليف' },
    { id: 'custom', name: 'Custom', name_ar: 'تصميم خاص' }
  ];

  var CATEGORIES_BY_ID = {};
  CATEGORIES.forEach(function(c) { CATEGORIES_BY_ID[c.id] = c; });

  var SEED_PRODUCTS = [
    { id: 'p1', name: 'Premium Business Cards', name_ar: 'كروت شخصية بريميوم', description: 'Matte or glossy finish, 350gsm.', description_ar: 'خامة مطفية او لامعة 350 جرام', category: 'business_cards', base_price: 150, is_featured: true, discount_percentage: 0, image: 'IMAGE:business-cards-print' },
    { id: 'p2', name: 'A5 Flyers', name_ar: 'فلايرز A5', description: 'Vivid full color flyers.', description_ar: 'فلايرز ألوان كاملة', category: 'flyers', base_price: 200, is_featured: true, discount_percentage: 30, image: 'IMAGE:flyers-print' },
    { id: 'p3', name: 'Tri-fold Brochures', name_ar: 'بروشورات مطوية', description: 'Professional tri-fold layout.', description_ar: 'تصميم مطوي احترافي', category: 'brochures', base_price: 350, is_featured: false, discount_percentage: 0, image: 'IMAGE:brochure-print' },
    { id: 'p4', name: 'A2 Posters', name_ar: 'بوسترات A2', description: 'High resolution large format.', description_ar: 'طباعة عالية الدقة', category: 'posters', base_price: 120, is_featured: false, discount_percentage: 0, image: 'IMAGE:poster-print' },
    { id: 'p5', name: 'Branded Envelopes', name_ar: 'مظاريف مطبوعة', description: 'Custom printed envelopes.', description_ar: 'مظاريف بشعارك', category: 'envelopes', base_price: 180, is_featured: false, discount_percentage: 0, image: 'IMAGE:envelope-print' },
    { id: 'p6', name: 'Vinyl Stickers', name_ar: 'ستيكرز فينيل', description: 'Weatherproof vinyl stickers.', description_ar: 'ستيكرز مقاومة للماء', category: 'stickers', base_price: 90, is_featured: true, discount_percentage: 15, image: 'IMAGE:vinyl-stickers' },
    { id: 'p7', name: 'Spiral Notebooks', name_ar: 'دفاتر سلك', description: 'Custom cover notebooks.', description_ar: 'دفاتر بغلاف مخصص', category: 'notebooks', base_price: 45, is_featured: false, discount_percentage: 0, image: 'IMAGE:notebooks-print' },
    { id: 'p8', name: 'Block Notes Pads', name_ar: 'بلوك نوت', description: 'Sticky and standard block notes.', description_ar: 'بلوك نوت عادي ولاصق', category: 'block_notes', base_price: 60, is_featured: false, discount_percentage: 0, image: 'IMAGE:block-notes' },
    { id: 'p9', name: 'Restaurant Menus', name_ar: 'منيوهات مطاعم', description: 'Laminated durable menus.', description_ar: 'منيوهات مقاومة ومغلفة', category: 'menus', base_price: 250, is_featured: true, discount_percentage: 0, image: 'IMAGE:restaurant-menu-print' },
    { id: 'p10', name: 'Custom Books', name_ar: 'كتب مخصصة', description: 'Full custom bound books.', description_ar: 'كتب بتجليد كامل', category: 'books', base_price: 500, is_featured: false, discount_percentage: 0, image: 'IMAGE:book-printing' }
  ];

  var PRODUCTS_BY_ID = {};
  SEED_PRODUCTS.forEach(function(p) { PRODUCTS_BY_ID[p.id] = p; });

  var CALCULATOR_FIELDS_BY_CATEGORY = {
    business_cards: ['quantity', 'paper', 'gsm', 'sides', 'lamination'],
    flyers: ['quantity', 'size', 'paper', 'gsm', 'sides', 'color'],
    brochures: ['quantity', 'size', 'paper', 'gsm', 'folds', 'sides'],
    posters: ['quantity', 'size', 'paper', 'gsm'],
    stickers: ['quantity', 'size', 'lamination'],
    notebooks: ['quantity', 'size', 'pages', 'paper', 'cover', 'binding', 'lamination'],
    block_notes: ['quantity', 'size', 'pages', 'paper', 'cover', 'binding'],
    menus: ['quantity', 'size', 'paper', 'gsm', 'lamination', 'folds', 'binding'],
    books: ['quantity', 'size', 'pages', 'paper', 'gsm', 'cover', 'binding', 'lamination'],
    custom: ['quantity', 'size', 'notes']
  };

  var SIZE_OPTIONS = ['A6', 'A5', 'A4', 'A3', 'A2', 'Custom'];
  var PAPER_OPTIONS = ['Standard 80gsm', 'Glossy 150gsm', 'Matte 170gsm', 'Cardstock 300gsm'];
  var GSM_OPTIONS = ['80', '120', '150', '170', '250', '300', '350'];
  var COVER_OPTIONS = ['Soft Cover', 'Hard Cover', 'Laminated Cover'];
  var BINDING_OPTIONS = ['Spiral', 'Staple', 'Perfect Bound', 'Hardcover'];
  var LAMINATION_OPTIONS = ['None', 'Glossy', 'Matte'];

  var AI_SUGGESTED_PROMPTS = [
    'ساعدني أعمل منيو لمطعم',
    'عايز تصميم فلاير لعرض 30%',
    'إيه أفضل ورق للكروت؟',
    'عايز أعمل كتاب خاص بيا',
    'احسبلي تكلفة 500 فلاير'
  ];
  // @end:constants

  // @section:navigation-setup @depends:[]
  var Tab = createBottomTabNavigator();
  var Stack = createStackNavigator();
  // @end:navigation-setup

  // @section:fetch-utils @depends:[]
  function fetchWithTimeout(url, options, timeoutMs) {
    var controller = new AbortController();
    var timer = setTimeout(function() { controller.abort(); }, timeoutMs);
    var opts = Object.assign({}, options, { signal: controller.signal });
    return fetch(url, opts).then(
      function(response) { clearTimeout(timer); return response; },
      function(err) { clearTimeout(timer); throw err; }
    );
  }
  // @end:fetch-utils

  // @section:ThemeContext @depends:[theme]
  const ThemeContext = React.createContext({
    theme: { colors: { primary: primaryColor, accent: accentColor, background: backgroundColor, card: cardColor, textPrimary: textPrimary, textSecondary: textSecondary, border: '#F0E0EC', success: '#10B981', error: '#EF4444', warning: '#F59E0B' } },
    darkMode: false,
    toggleDarkMode: function() {},
    designStyle: designStyle
  });
  const ThemeProvider = function(props) {
    const lightTheme = useMemo(function() {
      return {
        colors: {
          primary: primaryColor,
          accent: accentColor,
          background: backgroundColor,
          card: cardColor,
          textPrimary: textPrimary,
          textSecondary: textSecondary,
          border: '#F0E0EC',
          success: '#10B981',
          error: '#EF4444',
          warning: '#F59E0B'
        }
      };
    }, []);
    const value = useMemo(function() {
      return { theme: lightTheme, darkMode: false, toggleDarkMode: function() {}, designStyle: designStyle };
    }, [lightTheme]);
    return React.createElement(ThemeContext.Provider, { value: value }, props.children);
  };
  const useTheme = function() { return useContext(ThemeContext); };
  // @end:ThemeContext

  // @section:CartContext @depends:[]
  const CartContext = React.createContext({ items: [], addItem: function() {}, removeItem: function() {}, updateQty: function() {}, clearCart: function() {} });
  const CartProvider = function(props) {
    var itemsState = useState([]);
    var items = itemsState[0];
    var setItems = itemsState[1];

    var addItem = useCallback(function(item) {
      setItems(function(prev) { return prev.concat([item]); });
    }, []);
    var removeItem = useCallback(function(itemId) {
      setItems(function(prev) { return prev.filter(function(i) { return i.id !== itemId; }); });
    }, []);
    var updateQty = useCallback(function(itemId, qty) {
      setItems(function(prev) {
        return prev.map(function(i) { return i.id === itemId ? Object.assign({}, i, { quantity: qty }) : i; });
      });
    }, []);
    var clearCart = useCallback(function() { setItems([]); }, []);

    var value = useMemo(function() {
      return { items: items, addItem: addItem, removeItem: removeItem, updateQty: updateQty, clearCart: clearCart };
    }, [items, addItem, removeItem, updateQty, clearCart]);

    return React.createElement(CartContext.Provider, { value: value }, props.children);
  };
  const useCart = function() { return useContext(CartContext); };
  // @end:CartContext

  // @section:pricing-logic @depends:[constants]
  function computeItemPrice(product, options) {
    var base = product.base_price || 50;
    var qty = options.quantity || 1;
    var unitPrice = base;

    var gsm = parseInt(options.gsm || '150', 10);
    if (gsm > 200) { unitPrice += (gsm - 200) * 0.05; }

    if (options.sides === 'double') { unitPrice *= 1.4; }
    if (options.color === 'color') { unitPrice *= 1.3; }
    if (options.lamination && options.lamination !== 'None') { unitPrice += 5; }
    if (options.cover === 'Hard Cover') { unitPrice += 20; }
    if (options.cover === 'Laminated Cover') { unitPrice += 10; }
    if (options.binding === 'Hardcover') { unitPrice += 25; }
    if (options.binding === 'Spiral') { unitPrice += 5; }
    if (options.pages) { unitPrice += parseInt(options.pages, 10) * 0.8; }
    if (options.folds) { unitPrice += parseInt(options.folds, 10) * 2; }
    if (options.size === 'A3') { unitPrice *= 1.3; }
    if (options.size === 'A2') { unitPrice *= 1.6; }
    if (options.size === 'Custom') { unitPrice *= 1.5; }

    var discount = product.discount_percentage ? (unitPrice * qty) * (product.discount_percentage / 100) : 0;
    var subtotal = unitPrice * qty;
    var total = subtotal - discount;

    return {
      unitPrice: Math.round(unitPrice * 100) / 100,
      subtotal: Math.round(subtotal * 100) / 100,
      discount: Math.round(discount * 100) / 100,
      total: Math.round(total * 100) / 100
    };
  }
  // @end:pricing-logic

  // @section:HomeScreen-Header @depends:[styles]
  var HomeHeader = function(props) {
    var theme = props.theme;
    var insets = props.insets;
    return React.createElement(View, { style: [styles.heroSection, { paddingTop: insets.top + 20, backgroundColor: theme.colors.primary }], componentId: 'home-hero' },
      React.createElement(Text, { style: styles.heroLogo, componentId: 'home-logo' }, 'PRINT FLASH'),
      React.createElement(Text, { style: styles.heroTagline, componentId: 'home-tagline' }, 'PRINT MORE — SAVE MORE'),
      React.createElement(View, { style: styles.heroBadge, componentId: 'home-offer-badge' },
        React.createElement(Text, { style: styles.heroBadgeText }, '30% OFF Selected Products')
      ),
      React.createElement(TouchableOpacity, { style: styles.heroCta, componentId: 'home-cta-offer' },
        React.createElement(Text, { style: [styles.heroCtaText, { color: theme.colors.primary }] }, 'Claim Your Offer Today')
      )
    );
  };
  // @end:HomeScreen-Header

  // @section:HomeScreen-Categories @depends:[styles,constants]
  var CategoryChip = function(props) {
    var theme = props.theme;
    var active = props.active;
    return React.createElement(TouchableOpacity, {
      style: [styles.categoryChip, { backgroundColor: active ? theme.colors.primary : theme.colors.card, borderColor: theme.colors.primary }],
      onPress: props.onPress,
      componentId: 'category-chip-' + props.item.id
    },
      React.createElement(Text, { style: { color: active ? '#FFFFFF' : theme.colors.primary, fontWeight: '600', fontSize: 13 } }, props.item.name)
    );
  };
  // @end:HomeScreen-Categories

  // @section:ProductCard @depends:[styles]
  var ProductCard = function(props) {
    var theme = props.theme;
    var product = props.product;
    return React.createElement(TouchableOpacity, {
      style: [styles.productCard, { backgroundColor: theme.colors.card }],
      onPress: function() { props.onPress(product); },
      componentId: 'product-card-' + product.id
    },
      React.createElement(Image, { source: { uri: product.image }, style: styles.productImage, componentId: 'product-image-' + product.id }),
      product.discount_percentage > 0 ? React.createElement(View, { style: [styles.discountBadge, { backgroundColor: theme.colors.accent }] },
        React.createElement(Text, { style: styles.discountBadgeText }, '-' + product.discount_percentage + '%')
      ) : null,
      React.createElement(View, { style: { padding: 12 } },
        React.createElement(Text, { style: [styles.productName, { color: theme.colors.textPrimary }] }, product.name),
        React.createElement(Text, { style: [styles.productCategory, { color: theme.colors.textSecondary }] }, CATEGORIES_BY_ID[product.category] ? CATEGORIES_BY_ID[product.category].name : product.category),
        React.createElement(Text, { style: [styles.productPrice, { color: theme.colors.primary }] }, 'From EGP ' + product.base_price)
      )
    );
  };
  // @end:ProductCard

  // @section:HomeScreen-state @depends:[ThemeContext]
  var useHomeScreenState = function() {
    var themeContext = useTheme();
    var theme = themeContext.theme;
    var catState = useState('all');
    var selectedCategory = catState[0];
    var setSelectedCategory = catState[1];
    var searchState = useState('');
    var searchText = searchState[0];
    var setSearchText = searchState[1];
    return { theme: theme, selectedCategory: selectedCategory, setSelectedCategory: setSelectedCategory, searchText: searchText, setSearchText: setSearchText };
  };
  // @end:HomeScreen-state

  // @section:HomeScreen @depends:[HomeScreen-state,HomeScreen-Header,HomeScreen-Categories,ProductCard,styles]
  var HomeScreen = function(props) {
    var navigation = props.navigation;
    var state = useHomeScreenState();
    var insets = useSafeAreaInsets();
    var scrollBottomPadding = Platform.OS === 'web' ? WEB_TAB_MENU_PADDING : (TAB_MENU_HEIGHT + insets.bottom + SCROLL_EXTRA_PADDING);

    var filteredProducts = useMemo(function() {
      return SEED_PRODUCTS.filter(function(p) {
        var matchCat = state.selectedCategory === 'all' || p.category === state.selectedCategory;
        var matchSearch = !state.searchText || p.name.toLowerCase().indexOf(state.searchText.toLowerCase()) !== -1;
        return matchCat && matchSearch;
      });
    }, [state.selectedCategory, state.searchText]);

    var featured = useMemo(function() {
      return SEED_PRODUCTS.filter(function(p) { return p.is_featured; });
    }, []);

    var handleProductPress = function(product) {
      navigation.push('ProductDetail', { productId: product.id });
    };

    return React.createElement(View, { style: { flex: 1, backgroundColor: state.theme.colors.background } },
      React.createElement(StatusBar, { backgroundColor: state.theme.colors.primary, barStyle: 'light-content' }),
      React.createElement(ScrollView, {
        style: { flex: 1 },
        contentContainerStyle: { paddingBottom: scrollBottomPadding }
      },
        React.createElement(HomeHeader, { theme: state.theme, insets: insets }),
        React.createElement(View, { style: styles.searchWrap },
          React.createElement(Ionicons, { name: 'search', size: 18, color: state.theme.colors.textSecondary }),
          React.createElement(TextInput, {
            style: styles.searchInput,
            placeholder: 'Search products...',
            placeholderTextColor: state.theme.colors.textSecondary,
            value: state.searchText,
            onChangeText: state.setSearchText,
            componentId: 'home-search-input'
          })
        ),
        React.createElement(View, { style: styles.sectionHeaderRow },
          React.createElement(Text, { style: [styles.sectionTitle, { color: state.theme.colors.textPrimary }] }, 'Special Offers'),
        ),
        React.createElement(ScrollView, { horizontal: true, showsHorizontalScrollIndicator: false, style: { flexGrow: 'initial' }, contentContainerStyle: { paddingHorizontal: 16 } },
          featured.map(function(p) {
            return React.createElement(View, { key: p.id, style: { marginRight: 12, width: 160 } },
              React.createElement(ProductCard, { theme: state.theme, product: p, onPress: handleProductPress })
            );
          })
        ),
        React.createElement(View, { style: styles.calcCtaRow },
          React.createElement(TouchableOpacity, {
            style: [styles.calcCtaButton, { backgroundColor: state.theme.colors.accent }],
            onPress: function() { navigation.navigate('Calculator'); },
            componentId: 'home-calc-cta'
          },
            React.createElement(MaterialIcons, { name: 'calculate', size: 20, color: '#FFFFFF' }),
            React.createElement(Text, { style: styles.calcCtaText }, 'Calculate Your Price')
          ),
          React.createElement(TouchableOpacity, {
            style: [styles.calcCtaButton, { backgroundColor: state.theme.colors.primary }],
            onPress: function() { navigation.navigate('AIAssistant'); },
            componentId: 'home-ai-cta'
          },
            React.createElement(Ionicons, { name: 'sparkles', size: 20, color: '#FFFFFF' }),
            React.createElement(Text, { style: styles.calcCtaText }, 'Chat with Print Flash AI')
          )
        ),
        React.createElement(View, { style: styles.sectionHeaderRow },
          React.createElement(Text, { style: [styles.sectionTitle, { color: state.theme.colors.textPrimary }] }, 'Services')
        ),
        React.createElement(ScrollView, { horizontal: true, showsHorizontalScrollIndicator: false, style: { flexGrow: 'initial' }, contentContainerStyle: { paddingHorizontal: 16 } },
          React.createElement(CategoryChip, { theme: state.theme, item: { id: 'all', name: 'All' }, active: state.selectedCategory === 'all', onPress: function() { state.setSelectedCategory('all'); } }),
          CATEGORIES.map(function(c) {
            return React.createElement(CategoryChip, { key: c.id, theme: state.theme, item: c, active: state.selectedCategory === c.id, onPress: function() { state.setSelectedCategory(c.id); } });
          })
        ),
        React.createElement(View, { style: styles.productGrid },
          filteredProducts.map(function(p) {
            return React.createElement(View, { key: p.id, style: styles.productGridItem },
              React.createElement(ProductCard, { theme: state.theme, product: p, onPress: handleProductPress })
            );
          })
        ),
        React.createElement(View, { style: styles.sectionHeaderRow },
          React.createElement(Text, { style: [styles.sectionTitle, { color: state.theme.colors.textPrimary }] }, 'Why Print Flash')
        ),
        React.createElement(View, { style: { paddingHorizontal: 16 } },
          ['Premium quality', 'Fast delivery', 'Competitive prices', 'Custom designs', 'Professional support'].map(function(reason, idx) {
            return React.createElement(View, { key: String(idx), style: styles.reasonRow },
              React.createElement(Ionicons, { name: 'checkmark-circle', size: 20, color: state.theme.colors.primary }),
              React.createElement(Text, { style: { marginLeft: 8, color: state.theme.colors.textPrimary, fontSize: 15 } }, reason)
            );
          })
        )
      )
    );
  };
  // @end:HomeScreen

  // @section:ProductDetailScreen @depends:[styles,pricing-logic]
  var ProductDetailScreen = function(props) {
    var navigation = props.navigation;
    var route = props.route;
    var themeContext = useTheme();
    var theme = themeContext.theme;
    var cart = useCart();
    var insets = useSafeAreaInsets();
    var productId = route && route.params ? route.params.productId : null;
    var product = productId ? PRODUCTS_BY_ID[productId] : SEED_PRODUCTS[0];

    var qtyState = useState('1');
    var quantity = qtyState[0];
    var setQuantity = qtyState[1];

    var priceInfo = useMemo(function() {
      return computeItemPrice(product, { quantity: parseInt(quantity || '1', 10) });
    }, [product, quantity]);

    var handleAddToCart = function() {
      cart.addItem({
        id: 'cart_' + Date.now(),
        productId: product.id,
        name: product.name,
        quantity: parseInt(quantity || '1', 10),
        unitPrice: priceInfo.unitPrice,
        total: priceInfo.total,
        options: {}
      });
      Platform.OS === 'web' ? window.alert('Added to cart') : Alert.alert('Added to cart');
    };

    return React.createElement(ScrollView, { style: { flex: 1, backgroundColor: theme.colors.background }, contentContainerStyle: { paddingTop: insets.top + 16, paddingBottom: insets.bottom + SCROLL_EXTRA_PADDING } },
      React.createElement(TouchableOpacity, { onPress: function() { navigation.goBack(); }, style: { paddingHorizontal: 16, marginBottom: 8 }, componentId: 'product-detail-back' },
        React.createElement(Ionicons, { name: 'arrow-back', size: 24, color: theme.colors.textPrimary })
      ),
      React.createElement(Image, { source: { uri: product.image }, style: styles.detailImage, componentId: 'product-detail-image' }),
      React.createElement(View, { style: { padding: 16 } },
        React.createElement(Text, { style: [styles.detailTitle, { color: theme.colors.textPrimary }] }, product.name),
        React.createElement(Text, { style: { color: theme.colors.textSecondary, marginBottom: 12 } }, product.description),
        React.createElement(Text, { style: [styles.detailPrice, { color: theme.colors.primary }] }, 'EGP ' + priceInfo.unitPrice + ' / unit'),
        React.createElement(View, { style: styles.qtyRow },
          React.createElement(Text, { style: { color: theme.colors.textPrimary, fontSize: 15 } }, 'Quantity'),
          React.createElement(TextInput, {
            style: [styles.qtyInput, { borderColor: theme.colors.border, color: theme.colors.textPrimary }],
            value: quantity,
            onChangeText: function(t) { setQuantity(t.replace(/[^0-9]/g, '')); },
            keyboardType: 'numeric',
            componentId: 'product-detail-qty-input'
          })
        ),
        React.createElement(View, { style: [styles.priceSummaryCard, { backgroundColor: theme.colors.card }] },
          React.createElement(Text, { style: styles.summaryRowText }, 'Subtotal: EGP ' + priceInfo.subtotal),
          React.createElement(Text, { style: styles.summaryRowText }, 'Discount: EGP ' + priceInfo.discount),
          React.createElement(Text, { style: [styles.summaryRowText, { fontWeight: 'bold' }] }, 'Total: EGP ' + priceInfo.total)
        ),
        React.createElement(TouchableOpacity, { style: [styles.primaryButton, { backgroundColor: theme.colors.primary }], onPress: handleAddToCart, componentId: 'product-detail-add-cart' },
          React.createElement(Text, { style: styles.primaryButtonText }, 'Add to Cart')
        )
      )
    );
  };
  // @end:ProductDetailScreen

  // @section:CalculatorScreen-state @depends:[ThemeContext,constants]
  var useCalculatorState = function() {
    var themeContext = useTheme();
    var theme = themeContext.theme;
    var catState = useState('flyers');
    var category = catState[0];
    var setCategory = catState[1];
    var optionsState = useState({ quantity: '100', size: 'A5', paper: PAPER_OPTIONS[0], gsm: '150', sides: 'single', color: 'color', folds: '1', pages: '20', cover: COVER_OPTIONS[0], binding: BINDING_OPTIONS[0], lamination: LAMINATION_OPTIONS[0], notes: '' });
    var options = optionsState[0];
    var setOptions = optionsState[1];
    return { theme: theme, category: category, setCategory: setCategory, options: options, setOptions: setOptions };
  };
  // @end:CalculatorScreen-state

  // @section:CalculatorScreen-handlers @depends:[CalculatorScreen-state]
  var calculatorScreenHandlers = {
    setField: function(state, field, value) {
      state.setOptions(function(prev) { return Object.assign({}, prev, field, value) ; });
    }
  };
  // Fix: proper flat handler taking field & value
  calculatorScreenHandlers.setField = function(state, field, value) {
    state.setOptions(function(prev) {
      var next = Object.assign({}, prev);
      next[field] = value;
      return next;
    });
  };
  // @end:CalculatorScreen-handlers

  // @section:CalculatorScreen-OptionPicker @depends:[styles]
  var OptionPicker = function(props) {
    var theme = props.theme;
    return React.createElement(View, { style: { marginBottom: 14 } },
      React.createElement(Text, { style: [styles.fieldLabel, { color: theme.colors.textPrimary }] }, props.label),
      React.createElement(ScrollView, { horizontal: true, showsHorizontalScrollIndicator: false, style: { flexGrow: 'initial' } },
        props.options.map(function(opt) {
          var active = props.value === opt;
          return React.createElement(TouchableOpacity, {
            key: opt,
            style: [styles.optionChip, { backgroundColor: active ? theme.colors.primary : theme.colors.card, borderColor: theme.colors.primary }],
            onPress: function() { props.onSelect(opt); },
            componentId: 'option-chip-' + props.label + '-' + opt
          }, React.createElement(Text, { style: { color: active ? '#FFFFFF' : theme.colors.primary, fontSize: 13, fontWeight: '600' } }, opt));
        })
      )
    );
  };
  // @end:CalculatorScreen-OptionPicker

  // @section:CalculatorScreen @depends:[CalculatorScreen-state,CalculatorScreen-handlers,CalculatorScreen-OptionPicker,styles,pricing-logic]
  var CalculatorScreen = function(props) {
    var navigation = props.navigation;
    var state = useCalculatorState();
    var handlers = calculatorScreenHandlers;
    var cart = useCart();
    var insets = useSafeAreaInsets();
    var scrollBottomPadding = Platform.OS === 'web' ? WEB_TAB_MENU_PADDING : (TAB_MENU_HEIGHT + insets.bottom + SCROLL_EXTRA_PADDING);

    var fields = CALCULATOR_FIELDS_BY_CATEGORY[state.category] || [];
    var pseudoProduct = useMemo(function() {
      var found = SEED_PRODUCTS.find(function(p) { return p.category === state.category; });
      return found || SEED_PRODUCTS[0];
    }, [state.category]);

    var priceInfo = useMemo(function() {
      var opts = Object.assign({}, state.options, { quantity: parseInt(state.options.quantity || '1', 10) });
      return computeItemPrice(pseudoProduct, opts);
    }, [state.options, pseudoProduct]);

    var handleAddToCart = function() {
      cart.addItem({
        id: 'calc_' + Date.now(),
        productId: pseudoProduct.id,
        name: (CATEGORIES_BY_ID[state.category] ? CATEGORIES_BY_ID[state.category].name : state.category) + ' (Custom Spec)',
        quantity: parseInt(state.options.quantity || '1', 10),
        unitPrice: priceInfo.unitPrice,
        total: priceInfo.total,
        options: state.options
      });
      Platform.OS === 'web' ? window.alert('Added to cart') : Alert.alert('Added to cart');
    };

    return React.createElement(View, { style: { flex: 1, backgroundColor: state.theme.colors.background } },
      React.createElement(StatusBar, { backgroundColor: state.theme.colors.primary, barStyle: 'light-content' }),
      React.createElement(View, { style: [styles.simpleHeader, { paddingTop: insets.top + 12, backgroundColor: state.theme.colors.primary }] },
        React.createElement(Text, { style: styles.simpleHeaderTitle }, 'Price Calculator')
      ),
      React.createElement(ScrollView, { style: { flex: 1 }, contentContainerStyle: { padding: 16, paddingBottom: scrollBottomPadding } },
        React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Product Category'),
        React.createElement(ScrollView, { horizontal: true, showsHorizontalScrollIndicator: false, style: { flexGrow: 'initial', marginBottom: 16 } },
          CATEGORIES.filter(function(c) { return CALCULATOR_FIELDS_BY_CATEGORY[c.id]; }).map(function(c) {
            var active = state.category === c.id;
            return React.createElement(TouchableOpacity, {
              key: c.id,
              style: [styles.optionChip, { backgroundColor: active ? state.theme.colors.accent : state.theme.colors.card, borderColor: state.theme.colors.accent }],
              onPress: function() { state.setCategory(c.id); },
              componentId: 'calc-category-' + c.id
            }, React.createElement(Text, { style: { color: active ? '#FFFFFF' : state.theme.colors.accent, fontWeight: '600', fontSize: 13 } }, c.name));
          })
        ),
        fields.indexOf('quantity') !== -1 ? React.createElement(View, { style: { marginBottom: 14 } },
          React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Quantity'),
          React.createElement(TextInput, {
            style: [styles.textInputBox, { borderColor: state.theme.colors.border, color: state.theme.colors.textPrimary }],
            value: state.options.quantity,
            onChangeText: function(t) { handlers.setField(state, 'quantity', t.replace(/[^0-9]/g, '')); },
            keyboardType: 'numeric',
            componentId: 'calc-quantity-input'
          })
        ) : null,
        fields.indexOf('size') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Size', options: SIZE_OPTIONS, value: state.options.size, onSelect: function(v) { handlers.setField(state, 'size', v); } }) : null,
        fields.indexOf('paper') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Paper Type', options: PAPER_OPTIONS, value: state.options.paper, onSelect: function(v) { handlers.setField(state, 'paper', v); } }) : null,
        fields.indexOf('gsm') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'GSM', options: GSM_OPTIONS, value: state.options.gsm, onSelect: function(v) { handlers.setField(state, 'gsm', v); } }) : null,
        fields.indexOf('sides') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Sides', options: ['single', 'double'], value: state.options.sides, onSelect: function(v) { handlers.setField(state, 'sides', v); } }) : null,
        fields.indexOf('color') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Color', options: ['color', 'bw'], value: state.options.color, onSelect: function(v) { handlers.setField(state, 'color', v); } }) : null,
        fields.indexOf('folds') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Number of Folds', options: ['0', '1', '2', '3'], value: state.options.folds, onSelect: function(v) { handlers.setField(state, 'folds', v); } }) : null,
        fields.indexOf('pages') !== -1 ? React.createElement(View, { style: { marginBottom: 14 } },
          React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Number of Pages'),
          React.createElement(TextInput, {
            style: [styles.textInputBox, { borderColor: state.theme.colors.border, color: state.theme.colors.textPrimary }],
            value: state.options.pages,
            onChangeText: function(t) { handlers.setField(state, 'pages', t.replace(/[^0-9]/g, '')); },
            keyboardType: 'numeric',
            componentId: 'calc-pages-input'
          })
        ) : null,
        fields.indexOf('cover') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Cover Type', options: COVER_OPTIONS, value: state.options.cover, onSelect: function(v) { handlers.setField(state, 'cover', v); } }) : null,
        fields.indexOf('binding') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Binding', options: BINDING_OPTIONS, value: state.options.binding, onSelect: function(v) { handlers.setField(state, 'binding', v); } }) : null,
        fields.indexOf('lamination') !== -1 ? React.createElement(OptionPicker, { theme: state.theme, label: 'Lamination', options: LAMINATION_OPTIONS, value: state.options.lamination, onSelect: function(v) { handlers.setField(state, 'lamination', v); } }) : null,
        fields.indexOf('notes') !== -1 ? React.createElement(View, { style: { marginBottom: 14 } },
          React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Special Instructions'),
          React.createElement(TextInput, {
            style: [styles.textInputBox, { borderColor: state.theme.colors.border, color: state.theme.colors.textPrimary, height: 90 }],
            value: state.options.notes,
            onChangeText: function(t) { handlers.setField(state, 'notes', t); },
            multiline: true,
            numberOfLines: 4,
            textAlignVertical: 'top',
            componentId: 'calc-notes-input'
          })
        ) : null,
        React.createElement(View, { style: [styles.priceSummaryCard, { backgroundColor: state.theme.colors.card }] },
          React.createElement(Text, { style: [styles.summaryTitle, { color: state.theme.colors.textPrimary }] }, 'Price Breakdown'),
          React.createElement(Text, { style: styles.summaryRowText }, 'Subtotal: EGP ' + priceInfo.subtotal),
          React.createElement(Text, { style: styles.summaryRowText }, 'Discount: EGP ' + priceInfo.discount),
          React.createElement(Text, { style: styles.summaryRowText }, 'Delivery: EGP 0'),
          React.createElement(Text, { style: [styles.summaryRowText, { fontWeight: 'bold', fontSize: 18 }] }, 'Total: EGP ' + priceInfo.total)
        ),
        React.createElement(TouchableOpacity, { style: [styles.primaryButton, { backgroundColor: state.theme.colors.primary }], onPress: handleAddToCart, componentId: 'calc-add-cart' },
          React.createElement(Text, { style: styles.primaryButtonText }, 'Add to Cart')
        ),
        React.createElement(TouchableOpacity, { style: [styles.secondaryButton, { borderColor: state.theme.colors.primary }], onPress: function() { navigation.navigate('Cart'); }, componentId: 'calc-request-quote' },
          React.createElement(Text, { style: { color: state.theme.colors.primary, fontWeight: 'bold' } }, 'Request Custom Quote')
        )
      )
    );
  };
  // @end:CalculatorScreen

  // @section:AIMessage-Row @depends:[styles]
  var AIMessageRow = function(props) {
    var theme = props.theme;
    var message = props.message;
    var isUser = message.role === 'user';
    return React.createElement(View, { style: [styles.chatRow, { justifyContent: isUser ? 'flex-end' : 'flex-start' }] },
      React.createElement(View, { style: [styles.chatBubble, { backgroundColor: isUser ? theme.colors.primary : theme.colors.card, borderColor: theme.colors.border }] },
        React.createElement(Text, { style: { color: isUser ? '#FFFFFF' : theme.colors.textPrimary, fontSize: 14 } }, message.text)
      )
    );
  };
  // @end:AIMessage-Row

  // @section:AIAssistantScreen-state @depends:[ThemeContext]
  var useAIAssistantState = function() {
    var themeContext = useTheme();
    var theme = themeContext.theme;
    var messagesState = useState([{ id: 'welcome', role: 'ai', text: 'أهلاً بيك في Print Flash AI! اسألني عن أي حاجة في الطباعة والتصميم.' }]);
    var messages = messagesState[0];
    var setMessages = messagesState[1];
    var inputState = useState('');
    var inputText = inputState[0];
    var setInputText = inputState[1];
    var loadingState = useState(false);
    var loading = loadingState[0];
    var setLoading = loadingState[1];
    var errorState = useState(null);
    var error = errorState[0];
    var setError = errorState[1];
    return { theme: theme, messages: messages, setMessages: setMessages, inputText: inputText, setInputText: setInputText, loading: loading, setLoading: setLoading, error: error, setError: setError };
  };
  // @end:AIAssistantScreen-state

  // @section:AIAssistantScreen-handlers @depends:[AIAssistantScreen-state]
  var aiAssistantHandlers = {
    sendMessage: function(state, text) {
      if (!text || !text.trim()) { return; }
      var userMsg = { id: 'u_' + Date.now(), role: 'user', text: text };
      var updatedMessages = state.messages.concat([userMsg]);
      state.setMessages(updatedMessages);
      state.setInputText('');
      state.setLoading(true);
      state.setError(null);

      var apiMessages = updatedMessages.map(function(m) {
        return { role: m.role === 'ai' ? 'assistant' : 'user', content: m.text };
      });
      apiMessages.unshift({ role: 'system', content: 'You are Print Flash AI, a professional Arabic/English printing and design consultant helping customers with products, paper types, GSM, dimensions, finishing, quantities, and design/marketing ideas for a print shop called Print Flash.' });

      fetchWithTimeout('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + AppSecrets.OPENAI_API_KEY
        },
        body: JSON.stringify({ model: 'gpt-4o-mini', messages: apiMessages, max_tokens: 400 })
      }, 12000).then(function(response) {
        if (!response.ok) { throw new Error('HTTP ' + response.status); }
        return response.json();
      }).then(
        function(data) {
          var reply = data && data.choices && data.choices[0] && data.choices[0].message ? data.choices[0].message.content : 'عذراً، لم أستطع الرد الآن.';
          state.setMessages(function(prev) { return prev.concat([{ id: 'a_' + Date.now(), role: 'ai', text: reply }]); });
          state.setLoading(false);
        },
        function(err) {
          state.setError('Could not reach AI assistant. Please try again.');
          state.setLoading(false);
        }
      );
    },
    clearChat: function(state) {
      state.setMessages([{ id: 'welcome', role: 'ai', text: 'أهلاً بيك في Print Flash AI! اسألني عن أي حاجة في الطباعة والتصميم.' }]);
    }
  };
  // @end:AIAssistantScreen-handlers

  // @section:AIAssistantScreen @depends:[AIAssistantScreen-state,AIAssistantScreen-handlers,AIMessage-Row,styles,constants]
  var AIAssistantScreen = function(props) {
    var state = useAIAssistantState();
    var handlers = aiAssistantHandlers;
    var insets = useSafeAreaInsets();
    var scrollBottomPadding = Platform.OS === 'web' ? WEB_TAB_MENU_PADDING : (TAB_MENU_HEIGHT + insets.bottom + SCROLL_EXTRA_PADDING);

    return React.createElement(View, { style: { flex: 1, backgroundColor: state.theme.colors.background } },
      React.createElement(StatusBar, { backgroundColor: state.theme.colors.primary, barStyle: 'light-content' }),
      React.createElement(View, { style: [styles.simpleHeader, { paddingTop: insets.top + 12, backgroundColor: state.theme.colors.primary, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }] },
        React.createElement(Text, { style: styles.simpleHeaderTitle }, 'Print Flash AI'),
        React.createElement(TouchableOpacity, { onPress: function() { handlers.clearChat(state); }, componentId: 'ai-clear-chat' },
          React.createElement(Text, { style: { color: '#FFFFFF', fontSize: 13 } }, 'Clear Chat')
        )
      ),
      React.createElement(ScrollView, { style: { flex: 1 }, contentContainerStyle: { padding: 16, paddingBottom: scrollBottomPadding } },
        state.messages.map(function(m) {
          return React.createElement(AIMessageRow, { key: m.id, theme: state.theme, message: m });
        }),
        state.loading ? React.createElement(View, { style: { alignItems: 'flex-start', marginTop: 4 } },
          React.createElement(ActivityIndicator, { size: 'small', color: state.theme.colors.primary, componentId: 'ai-typing-indicator' })
        ) : null,
        state.error ? React.createElement(Text, { style: { color: state.theme.colors.error, marginTop: 8 } }, state.error) : null,
        React.createElement(View, { style: { marginTop: 16 } },
          React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Suggested Prompts'),
          AI_SUGGESTED_PROMPTS.map(function(prompt, idx) {
            return React.createElement(TouchableOpacity, {
              key: String(idx),
              style: [styles.promptChip, { borderColor: state.theme.colors.primary }],
              onPress: function() { handlers.sendMessage(state, prompt); },
              componentId: 'ai-suggested-prompt-' + idx
            }, React.createElement(Text, { style: { color: state.theme.colors.primary, fontSize: 13 } }, prompt));
          })
        )
      ),
      React.createElement(View, { style: [styles.chatInputRow, { borderTopColor: state.theme.colors.border, paddingBottom: insets.bottom + 8 }] },
        React.createElement(TextInput, {
          style: [styles.chatInput, { color: state.theme.colors.textPrimary, borderColor: state.theme.colors.border }],
          placeholder: 'اكتب سؤالك هنا...',
          placeholderTextColor: state.theme.colors.textSecondary,
          value: state.inputText,
          onChangeText: state.setInputText,
          componentId: 'ai-chat-input'
        }),
        React.createElement(TouchableOpacity, {
          style: [styles.chatSendButton, { backgroundColor: state.theme.colors.primary }],
          onPress: function() { handlers.sendMessage(state, state.inputText); },
          componentId: 'ai-chat-send'
        }, React.createElement(Ionicons, { name: 'send', size: 18, color: '#FFFFFF' }))
      )
    );
  };
  // @end:AIAssistantScreen

  // @section:CartScreen-Row @depends:[styles]
  var CartRow = function(props) {
    var theme = props.theme;
    var item = props.item;
    return React.createElement(View, { style: [styles.cartRow, { backgroundColor: theme.colors.card }] },
      React.createElement(View, { style: { flex: 1 } },
        React.createElement(Text, { style: { color: theme.colors.textPrimary, fontWeight: '600' } }, item.name),
        React.createElement(Text, { style: { color: theme.colors.textSecondary, fontSize: 13 } }, 'Qty: ' + item.quantity + ' • EGP ' + item.total)
      ),
      React.createElement(TouchableOpacity, { onPress: function() { props.onRemove(item.id); }, componentId: 'cart-remove-' + item.id },
        React.createElement(Ionicons, { name: 'trash', size: 20, color: theme.colors.error })
      )
    );
  };
  // @end:CartScreen-Row

  // @section:CartScreen-state @depends:[ThemeContext]
  var useCartScreenState = function() {
    var themeContext = useTheme();
    var theme = themeContext.theme;
    var couponState = useState('');
    var couponCode = couponState[0];
    var setCouponCode = couponState[1];
    var appliedDiscountState = useState(0);
    var appliedDiscount = appliedDiscountState[0];
    var setAppliedDiscount = appliedDiscountState[1];
    return { theme: theme, couponCode: couponCode, setCouponCode: setCouponCode, appliedDiscount: appliedDiscount, setAppliedDiscount: setAppliedDiscount };
  };
  // @end:CartScreen-state

  // @section:CartScreen-handlers @depends:[CartScreen-state]
  var cartScreenHandlers = {
    applyCoupon: function(state) {
      if (state.couponCode.trim().toUpperCase() === 'PRINT30') {
        state.setAppliedDiscount(30);
        Platform.OS === 'web' ? window.alert('Coupon applied: 30% off') : Alert.alert('Coupon applied: 30% off');
      } else {
        state.setAppliedDiscount(0);
        Platform.OS === 'web' ? window.alert('Invalid coupon code') : Alert.alert('Invalid coupon code');
      }
    }
  };
  // @end:CartScreen-handlers

  // @section:CartScreen @depends:[CartScreen-state,CartScreen-handlers,CartScreen-Row,styles]
  var CartScreen = function(props) {
    var navigation = props.navigation;
    var cart = useCart();
    var state = useCartScreenState();
    var handlers = cartScreenHandlers;
    var insets = useSafeAreaInsets();
    var scrollBottomPadding = Platform.OS === 'web' ? WEB_TAB_MENU_PADDING : (TAB_MENU_HEIGHT + insets.bottom + SCROLL_EXTRA_PADDING);

    var subtotal = useMemo(function() {
      return cart.items.reduce(function(sum, i) { return sum + i.total; }, 0);
    }, [cart.items]);
    var discountAmount = subtotal * (state.appliedDiscount / 100);
    var deliveryFee = cart.items.length > 0 ? 30 : 0;
    var total = subtotal - discountAmount + deliveryFee;

    return React.createElement(View, { style: { flex: 1, backgroundColor: state.theme.colors.background } },
      React.createElement(StatusBar, { backgroundColor: state.theme.colors.primary, barStyle: 'light-content' }),
      React.createElement(View, { style: [styles.simpleHeader, { paddingTop: insets.top + 12, backgroundColor: state.theme.colors.primary }] },
        React.createElement(Text, { style: styles.simpleHeaderTitle }, 'My Cart')
      ),
      React.createElement(ScrollView, { style: { flex: 1 }, contentContainerStyle: { padding: 16, paddingBottom: scrollBottomPadding } },
        cart.items.length === 0 ? React.createElement(Text, { style: { color: state.theme.colors.textSecondary, textAlign: 'center', marginTop: 40 } }, 'Your cart is empty') :
          cart.items.map(function(item) {
            return React.createElement(CartRow, { key: item.id, theme: state.theme, item: item, onRemove: cart.removeItem });
          }),
        cart.items.length > 0 ? React.createElement(View, { style: { marginTop: 16 } },
          React.createElement(Text, { style: [styles.fieldLabel, { color: state.theme.colors.textPrimary }] }, 'Coupon Code'),
          React.createElement(View, { style: { flexDirection: 'row' } },
            React.createElement(TextInput, {
              style: [styles.textInputBox, { flex: 1, marginRight: 8, borderColor: state.theme.colors.border, color: state.theme.colors.textPrimary }],
              value: state.couponCode,
              onChangeText: state.setCouponCode,
              autoCapitalize: 'characters',
              placeholder: 'PRINT30',
              placeholderTextColor: state.theme.colors.textSecondary,
              componentId: 'cart-coupon-input'
            }),
            React.createElement(TouchableOpacity, { style: [styles.applyButton, { backgroundColor: state.theme.colors.accent }], onPress: function() { handlers.applyCoupon(state); }, componentId: 'cart-apply-coupon' },
              React.createElement(Text, { style: { color: '#FFFFFF', fontWeight: '600' } }, 'Apply')
            )
          ),
          React.createElement(View, { style: [styles.priceSummaryCard, { backgroundColor: state.theme.colors.card, marginTop: 16 }] },
            React.createElement(Text, { style: styles.summaryRowText }, 'Subtotal: EGP ' + subtotal.toFixed(2)),
            React.createElement(Text, { style: styles.summaryRowText }, 'Discount: EGP ' + discountAmount.
