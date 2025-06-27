import { Link } from "expo-router";
import { View, Text, StyleSheet } from "react-native";

export default function HomeScreen() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>FastLibrarian</Text>
      <Link href="/authors" style={styles.link}>
        Authors
      </Link>
      <Link href="/books" style={styles.link}>
        Books
      </Link>
      <Link href="/series" style={styles.link}>
        Series
      </Link>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: "center", justifyContent: "center" },
  title: { fontSize: 32, marginBottom: 32 },
  link: { fontSize: 20, marginVertical: 8, color: "#007AFF" },
});
