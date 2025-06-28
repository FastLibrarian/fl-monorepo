import { use, useEffect, useState } from "react";
import { sharedStyles as styles } from "../app/sharedstyles";

import { useLocalSearchParams, useRouter } from "expo-router";
import {
  View,
  Text,
  FlatList,
  ActivityIndicator,
  Pressable,
  ScrollView,
} from "react-native";

const API_URL = "http://localhost:8000/books";

interface Book {
  id: string;
  title: string;
  description: string | null;
  authors: { id: string; name: string }[];
  series: { id: string; name: string } | null;
  external_refs: Record<string, any> | null;
  status: string | null;
}

export default function BookScreen() {
  const { id } = useLocalSearchParams();
  const [book, setBook] = useState<Book | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchBook();
  }, [id]);
  const router = useRouter();
  const fetchBook = async () => {
    try {
      setLoading(true);
      setError(null);

      if (!id) {
        setError("Book ID is missing");
        setLoading(false);
        return;
      }

      const response = await fetch(`${API_URL}/${id}`);

      if (!response.ok) {
        throw new Error(`Error fetching book: ${response.statusText}`);
      }

      const data = await response.json();
      setBook(data);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch book details");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.title}>Loading book details...</Text>
      </View>
    );
  }
  if (error) {
    return (
      <View style={styles.container}>
        <Text style={{ color: "red" }}>{error}</Text>
      </View>
    );
  }
  if (!book) {
    return (
      <View style={styles.container}>
        <Text style={styles.title}>Book not found</Text>
      </View>
    );
  }
  return (
    <ScrollView style={styles.container}>
      <Text style={styles.title}>{book.title}</Text>
      <Text style={styles.description}>
        {book.description || "No description available"}
      </Text>
      <Text style={styles.subtitle}>Authors:</Text>
      <FlatList
        data={book.authors}
        keyExtractor={(author) => author.id}
        renderItem={({ item }) => (
          <Pressable
            onPress={() => router.navigate("author", { id: item.id })}
            style={styles.authorCard}
          >
            <Text style={styles.authorName}>{item.name}</Text>
          </Pressable>
        )}
      />
      {book.series && (
        <Text style={styles.subtitle}>Series: {book.series.name}</Text>
      )}
      {book.external_refs && (
        <View>
          <Text style={styles.subtitle}>External References:</Text>
          {Object.entries(book.external_refs).map(([key, value]) => (
            <Text key={key} style={styles.externalRef}>
              {key}: {value}
            </Text>
          ))}
        </View>
      )}
      <Pressable
        onPress={() => router.back()}
        style={[styles.button, styles.goBackButton]}
      >
        <Text style={{ color: "white" }}>Go Back</Text>
      </Pressable>
    </ScrollView>
  );
}
