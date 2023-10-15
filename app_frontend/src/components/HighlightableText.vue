<template>
    <div v-html="fullText" />
</template>
<script>

export default {
    props: {
        text: String,
        highlight: String,
    },
    computed: {
        fullText() {
            const text = this.text;
            const highlight = this.highlight;
            if (highlight) {
                const start = text.indexOf(highlight);
                const len = highlight.length;
                return [
                    text.substring(0, start),
                    "<strong>",
                    highlight,
                    "</strong>",
                    text.substring(start + len),
                ].join("");
            }
            return text;
        }
    }
}
</script>