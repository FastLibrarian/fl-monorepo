import React from "react";
import { View, Text, Pressable, StyleProp, ViewStyle } from "react-native";
import { sharedStyles as styles } from "../app/sharedstyles";
import { useRouter } from "expo-router";

interface BookCardProps {
  book: {
    id: string;
    title: string;
    description?: string | null;
    authors?: { id: string; name: string }[];
    series?:
      | { id: string; name: string }[]
      | { id: string; name: string }
      | null;
    status?: string | null;
  };
  onPressDetails?: () => void;
  showDetailsButton?: boolean;
  containerStyle?: StyleProp<ViewStyle>;
}

const BookCard: React.FC<BookCardProps> = ({
  book,
  onPressDetails,
  showDetailsButton = true,
  containerStyle,
}) => {
  const router = useRouter();
  // Support both array and single object for series
  const seriesList = Array.isArray(book.series)
    ? book.series
    : book.series
    ? [book.series]
    : [];

  const handlePress = onPressDetails
    ? onPressDetails
    : () => router.navigate({ pathname: "/book", params: { id: book.id } });

  return (
    <View style={[styles.card, containerStyle]}>
      <Text style={styles.primaryName}>{book.title}</Text>
      {book.authors && book.authors.length > 0 && (
        <Text style={styles.secondaryName}>
          {book.authors.map((a) => a.name).join(", ")}
        </Text>
      )}
      {book.description ? (
        <Text style={styles.primaryText}>{book.description}</Text>
      ) : (
        <Text style={styles.tertiaryText}>(No description)</Text>
      )}
      {seriesList.length > 0 && (
        <Text style={styles.secondaryName}>
          Series: {seriesList.map((s) => s.name).join(", ")}
        </Text>
      )}
      {showDetailsButton && (
        <Pressable onPress={handlePress} style={{ alignSelf: "flex-end" }}>
          <Text style={styles.addButton}>View Details</Text>
        </Pressable>
      )}
    </View>
  );
};

export default BookCard;
