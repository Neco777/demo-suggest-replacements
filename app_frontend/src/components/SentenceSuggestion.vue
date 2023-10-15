<template>
    <div class="sentence-suggestion">
        <highlightable-text :text="sentence.sentence" :highlight="hoveredText" />
        <div class="suggestion-area">
            <div v-if="sentence.suggestions.length > 0">
                <table>
                    <thead>
                        <th>Phrase</th>
                        <th>Replacement</th>
                        <th>Score</th>
                    </thead>
                    <phrase-suggestion
                        v-for="suggestion in sentence.suggestions"
                        :key="suggestion.original_phrase + suggestion.replacement"
                        :suggestion="suggestion"
                        @mouseover="hoveredSuggestion = suggestion"
                    />
                </table>
            </div>
            <div v-else>
                No suggestions for this sentence
            </div>
        </div>
    </div>
</template>

<script>
import HighlightableText from './HighlightableText.vue'
import PhraseSuggestion from './PhraseSuggestion.vue'
export default {
    components: { PhraseSuggestion, HighlightableText },
    props: {
        sentence: Object
    },
    data() {
        return {
            hoveredSuggestion: null,
        }
    },
    computed: {
        hoveredText() {
            if (this.hoveredSuggestion) {
                return this.hoveredSuggestion.original_phrase;
            }
        }
    }
}
</script>

<style>
.sentence-suggestion {
    margin-left: 10px;
    margin-bottom: 20px;
}
.suggestion-area {
    margin-left: 10px;
}

.suggestion-area table {
    border-collapse: collapse;
    width: 100%;
}

.suggestion-area table th {
    border: 1px solid black;
    background-color: rgb(66, 142, 255);
    color: white;
}

.suggestion-area table tr:hover {
    background-color: rgb(253, 224, 58);
}

.suggestion-area table td {
    border: 1px solid black;
}

</style>