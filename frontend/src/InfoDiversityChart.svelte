<script>
    export let message;
</script>

<div id="info" class="space-y-4">
    <h1>About this visualisation</h1>

    <p>This chart shows the mean sentiment of election-themed tweets against a measure of diversity in areas of Greater Melbourne.
        A line of best fit is also shown to examine correlation between diversity and attitude towards the election.
    </p>

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
