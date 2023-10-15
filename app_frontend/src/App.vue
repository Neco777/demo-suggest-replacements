<template>
  <div class="page">
    <div class="source">
      <label>Text</label>
      <textarea v-model="sourceText" type="text" />

      <label>Standard Phrases (one per line)</label>
      <textarea v-model="sourceStandardPhrasesRaw" placeholder="Put your phrases line by line"></textarea>

      <button @click="refreshData">Request suggestions</button>
    </div>
    <div class="output">
      <label>Suggestions</label>
      <div v-if="result">
        <div v-for="sentence in result" :key="sentence.sentence">
          <sentence-suggestion :sentence="sentence" />
        </div>
      </div>
      <div v-else>
        Loading...
      </div>
    </div>
  </div>
</template>

<script>

import SentenceSuggestion from './components/SentenceSuggestion.vue';

export default {
  components: { SentenceSuggestion },
  data() {
    return {
      // sourceText: "I love my cat",
      // sourceStandardPhrasesRaw: "tiny tiger\nlarge elephant",
      sourceText: "In today's meeting, we discussed a variety of issues affecting our department. " +
        "The weather was unusually sunny, a pleasant backdrop to our serious discussions." +
        "We came to the consensus that we need to do better in terms of performance." +
        "Sally brought doughnuts, which lightened the mood." +
        "It's important to make good use of what we have at our disposal." +
        "During the coffee break, we talked about the upcoming company picnic." +
        "We should aim to be more efficient and look for ways to be more creative in our daily tasks.",

      sourceStandardPhrasesRaw:
          "Optimal performance\n" +
          "Utilize resources\n" +
          "Enhance productivity\n" +
          "Conduct an analysis\n" +
          "Maintain a high standard\n" +
          "Implement best practices\n" +
          "Ensure compliance\n" +
          "Streamline operations\n" +
          "Foster innovation\n" +
          "Drive growth\n" +
          "Leverage synergies\n" +
          "Demonstrate leadership\n",
      result: null,
    }
  },
  computed: {
    sourceStandardPhrases() {
      return this.sourceStandardPhrasesRaw.split('\n').map(s => s.trim()).filter(s => s);
    }
  },
  async mounted() {
    this.refreshData().catch(err => {
      console.error(err);
    });
  },
  methods: {
    async refreshData() {
      this.result = null;
      const response = await fetch("http://localhost:8000/api/try-suggest", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
          "sentence": this.sourceText,
          "standard_phrases": this.sourceStandardPhrases,
        }),
      });
      this.result = await response.json();
    }
  },
}

</script>

<style scoped>
.page {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  align-self: flex-start;
}
.source{
  display: flex;
  flex-direction: column;
}

.label {
  margin-top: 10px;
}

.source textarea {
  height: 200px;
  width: 600px;
}
</style>

