import { View, Button, StyleSheet } from "react-native";
import { useRouter } from "expo-router";

const routes = [
  { name: "Home", path: "/" },
  { name: "Authors", path: "/authors" },
  { name: "Books", path: "/books" },
  { name: "Series", path: "/series" },
];

export default function Navbar() {
  const router = useRouter();
  return (
    <View style={styles.navbar}>
      {routes.map((route) => (
        <Button
          key={route.path}
          title={route.name}
          onPress={() => router.push(route.path)}

        />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  navbar: {
    flexDirection: "row",
    backgroundColor: "#007AFF",
    paddingTop: 16,
    paddingBottom: 16,
    justifyContent: "space-around",
    alignItems: "center",
  },
});