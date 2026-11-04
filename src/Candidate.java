import java.util.List;

/** Parsed statistics fields plus the original CSV row for lossless group exports. */
public record Candidate(List<String> row, String gender, String group,
                        double math, double english, double computer, double average) {
    public Candidate {
        row = List.copyOf(row);
    }
}
