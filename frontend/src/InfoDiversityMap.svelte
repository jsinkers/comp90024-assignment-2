<script>
    export let message;
</script>

<div id="info" class="space-y-4">
    <h1>About this visualisation</h1>

    <p>This map shows a measure of diversity across SA2 areas of Greater Melbourne. Election themed tweets are displayed
        as markers coloured by sentiment. The opacity of tweet markers represents the intensity of sentiment analysed in the tweet,
        with higher opacity indicating greater intensity.</p>

    <h2>How is diversity measured?</h2>
    <p>As a proxy for cultural diversity, we have used 2016 Census data on the proportion of people in an SA2 that speak
    a language other than English at home. We consider a higher proportion of people speaking languages other than English
    to indicate a higher level of cultural diversity.</p>

    <h2>What is SA2?</h2>
    <p> Statistical areas are a structure maintained by the Australian Bureau of Statistics to divide up Australia into useful
        statistical units. SA2s are the second-smallest such area, and are medium-sized areas that correspond to a community
        that interacts socially and economically. SA2s shown are based on 2016 boundaries.</p>

</div>

<style>
    #info {
        @apply font-sans;
    }
    h1 {
        font-size: 2rem;
        text-align: center;
    }

    h2 {
        font-size: 1.25rem;
    }
</style>
