<template>
    <tr @mouseover="upHere = true" @mouseleave="upHere = false">
        <td>{{ suggestion.original_phrase }}</td>
        <td>{{ suggestion.replacement }}</td>
        <td>{{ suggestion.similarity_score }}</td>
    </tr>
</template>

<script>

export default {
    props: {
        suggestion: Object
    },
    methods: {
        
    }
}
</script>

<style>

</style>