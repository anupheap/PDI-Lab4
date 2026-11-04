import java.io.BufferedWriter;
import java.io.IOException;
import java.io.PushbackReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

public final class Csv {
    private Csv() { }

    public static ArrayList<List<String>> read(Path file) throws IOException {
        ArrayList<List<String>> rows = new ArrayList<>();
        try (PushbackReader reader = new PushbackReader(
                Files.newBufferedReader(file, StandardCharsets.UTF_8), 1)) {
            ArrayList<String> row = new ArrayList<>();
            StringBuilder field = new StringBuilder();
            boolean quoted = false;
            boolean closedQuote = false;
            boolean first = true;
            int c;
            while ((c = reader.read()) != -1) {
                if (first && c == '\uFEFF') {
                    first = false;
                    continue;
                }
                first = false;
                if (quoted) {
                    if (c == '"') {
                        int next = reader.read();
                        if (next == '"') {
                            field.append('"');
                        } else {
                            quoted = false;
                            closedQuote = true;
                            if (next != -1) {
                                reader.unread(next);
                            }
                        }
                    } else {
                        field.append((char) c);
                    }
                } else if (c == ',' || c == '\r' || c == '\n') {
                    row.add(field.toString());
                    field.setLength(0);
                    closedQuote = false;
                    if (c != ',') {
                        rows.add(row);
                        row = new ArrayList<>();
                        if (c == '\r') {
                            int next = reader.read();
                            if (next != '\n' && next != -1) {
                                reader.unread(next);
                            }
                        }
                    }
                } else if (c == '"' && field.length() == 0 && !closedQuote) {
                    quoted = true;
                } else {
                    if (closedQuote || c == '"') {
                        throw new IOException("Invalid quoting in CSV record " + (rows.size() + 1));
                    }
                    field.append((char) c);
                }
            }
            if (quoted) {
                throw new IOException("Unclosed quoted CSV field in " + file);
            }
            if (!row.isEmpty() || field.length() > 0 || closedQuote) {
                row.add(field.toString());
                rows.add(row);
            }
        }
        return rows;
    }

    public static void write(Path file, List<? extends List<String>> rows) throws IOException {
        try (BufferedWriter writer = Files.newBufferedWriter(file, StandardCharsets.UTF_8)) {
            for (List<String> row : rows) {
                for (int i = 0; i < row.size(); i++) {
                    if (i > 0) {
                        writer.write(',');
                    }
                    String value = row.get(i);
                    if (value.contains(",") || value.contains("\"")
                            || value.contains("\n") || value.contains("\r")) {
                        writer.write('"');
                        writer.write(value.replace("\"", "\"\""));
                        writer.write('"');
                    } else {
                        writer.write(value);
                    }
                }
                writer.newLine();
            }
        }
    }
}
