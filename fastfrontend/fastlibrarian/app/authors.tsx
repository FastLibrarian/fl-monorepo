import { useRef, useEffect, useState } from "react";
import { sharedStyles as styles } from "../app/sharedstyles";
import { View, Text, TextInput, Button, FlatList, Pressable, Animated, Easing } from "react-native";

const API_URL = "http://localhost:8000/authors";
const FIND_AUTHORS_URL = API_URL + "/find_authors";



export default function AuthorsScreen() {
  const [searchFocused, setSearchFocused] = useState(false);
  const [authors, setAuthors] = useState([]);
  const [name, setName] = useState("");
  const [foundAuthors, setFoundAuthors] = useState([]);
  const [searching, setSearching] = useState(false);

  // Animation refs
  const overlayOpacity = useRef(new Animated.Value(0)).current;
  const overlayTranslateY = useRef(new Animated.Value(40)).current;
  const expandedInputRef = useRef<TextInput>(null);

  useEffect(() => {
    fetchAuthors();
  }, []);

  useEffect(() => {
    if (searchFocused) {
      Animated.parallel([
        Animated.timing(overlayOpacity, {
          toValue: 1,
          duration: 250,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease),
        }),
        Animated.timing(overlayTranslateY, {
          toValue: 0,
          duration: 250,
          useNativeDriver: true,
          easing: Easing.out(Easing.ease),
        }),
      ]).start(() => {
        // Focus the expanded input after animation
        expandedInputRef.current?.focus();
      });
    } else {
      Animated.parallel([
        Animated.timing(overlayOpacity, {
          toValue: 0,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease),
        }),
        Animated.timing(overlayTranslateY, {
          toValue: 40,
          duration: 200,
          useNativeDriver: true,
          easing: Easing.in(Easing.ease),
        }),
      ]).start();
    }
  }, [searchFocused, overlayOpacity, overlayTranslateY]);

  const fetchAuthors = async () => {
    const res = await fetch(API_URL);
    setAuthors(await res.json());
  };

  const findAuthors = async () => {
    setSearching(true);
    try {
      const res = await fetch(FIND_AUTHORS_URL + "?" + new URLSearchParams({ name: name }), {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setFoundAuthors(data);
    } catch (error) {
      console.error(error);
    } finally {
      setSearching(false);
    }
  };

  const handleAddToDB = async (author) => {
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(author),
      });
      if (res.ok) {
        fetchAuthors();
      }
    } catch (error) {
      console.error(error);
    }
  };


  return (
    <View style={styles.container}>
      <Text style={styles.title}>Authors</Text>
      <FlatList
        data={authors}
        keyExtractor={item => item.id.toString()}
        renderItem={({ item }) => (
          <View style={styles.card}>
            <Text style={styles.authorName}>{item.name}</Text>
            <Text style={styles.authorBio}>{item.bio}</Text>
          </View>
        )}
      />

      {/* Animated Overlay for Find Authors */}
      <Animated.View
        pointerEvents={searchFocused ? "auto" : "none"}
        style={[
          styles.searchOverlay,
          {
            opacity: overlayOpacity,
            transform: [{ translateY: overlayTranslateY }],
            // Hide overlay visually when not focused
            display: searchFocused || overlayOpacity.__getValue() > 0 ? "flex" : "none",
          },
        ]}
      >
        <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
          <Text style={styles.subtitle}>Find Authors</Text>
          <Pressable onPress={() => setSearchFocused(false)} style={{ padding: 8 }}>
            <Text style={{ fontSize: 22 }}>▼</Text>
          </Pressable>
        </View>
        <TextInput
          ref={expandedInputRef}
          placeholder="Name"
          value={name}
          onChangeText={setName}
          style={styles.expandedSearchInput}
          onSubmitEditing={findAuthors}
        />
        <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
          <Button title={searching ? "Searching..." : "Find"} onPress={findAuthors} disabled={searching} />
        </View>
        <FlatList
          data={foundAuthors}
          keyExtractor={(item, idx) => (item.id ? item.id.toString() : "ext_" + idx)}
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.authorName}>{item.name}</Text>
              <Text style={styles.authorBio}>{item.bio}</Text>
              {item.in_db ? (
                <Text style={styles.inDbLabel}>(in DB)</Text>
              ) : (
                <Pressable onPress={() => handleAddToDB(item)}>
                  <Text style={styles.addButton}>Add to DB</Text>
                </Pressable>
              )}
            </View>
          )}
          ListEmptyComponent={foundAuthors.length === 0 && name ? <Text style={styles.item}>No authors found.</Text> : null}
        />
      </Animated.View>

      {/* Show the search bar only if overlay is not active */}
      {!searchFocused && (
        <>
          <Text style={styles.subtitle}>Find Authors</Text>
          <TextInput
            placeholder="Name"
            value={name}
            onChangeText={setName}
            style={styles.input}
            onFocus={() => setSearchFocused(true)}
            onSubmitEditing={findAuthors}
          />
          <View style={{ flexDirection: "row", alignItems: "center", justifyContent: "space-between" }}>
            <Button title={searching ? "Searching..." : "Find"} onPress={findAuthors} disabled={searching} />
          </View>
          <FlatList
            data={foundAuthors}
            keyExtractor={(item, idx) => (item.id ? item.id.toString() : "ext_" + idx)}
            renderItem={({ item }) => (
              <View style={styles.card}>
                <Text style={styles.authorName}>{item.name}</Text>
                <Text style={styles.authorBio}>{item.bio}</Text>
                {item.in_db ? (
                  <Text style={styles.inDbLabel}>(in DB)</Text>
                ) : (
                  <Pressable onPress={() => handleAddToDB(item)}>
                    <Text style={styles.addButton}>Add to DB</Text>
                  </Pressable>
                )}
              </View>
            )}
            ListEmptyComponent={foundAuthors.length === 0 && name ? <Text style={styles.item}>No authors found.</Text> : null}
          />
        </>
      )}
    </View>
  );
}
