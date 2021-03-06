FacebookAntiBully

What is FacebookAntiBully?

Far too often, social media serves as a prime stage for individuals to be victims of cyber bullying. Public forums such as Facebook are perfect for predators to seek out individuals and to post demeaning/belittling comments that can often times wreak havoc on a person's emotional/mental state. FacebookAntiBully is the first step towards ending the cycle of cyber bullying by protecting a user from any comments that are found to be any involving any form of cyber bullying. By immediately detecting and removing these posts from a user's wall, we are effectively preventing the bully from getting the gratification that often leads to continued offenses of bullying towards the same or other individual.

How does FacebookAntiBully Work?

Facebook anti bully leverages the Graph API provided by Facebook in order to respond to any updates to a user's wall. Any new posts or comments made to a pre-existing post trigger an event handled by the FacebookAntiBully software. The post is examined is for a series of keywords or phrases, taking into account context and if a post is flagged, it is promptly deleted from the user's wall, avoiding any hurtful effects from the remark.

What was used to create FacebookAntiBully?

FacebookAntiBully was created using a combination of the requests module as well as Flask to create a micro-framework to respond to any requests posted by the Facebook Graph API.

Changes for the Future?

In its current implementation, FacebookAntiBully serves only to demonstrate the autonomous moderation potential that can help put an end to the ever prevalent occurrences of cyber bullying that take place on a daily basis. In its final implementation, FacebookAntiBully will authenticate with a user via a simple Facebook App, keeping the experience entirely localized to the pre-existing Facebook infrastructure. In addition, adding the ability to enable this moderation technology as a parental control option would be an excellent asset to parents wishing to protect their children as they explore the internet. By putting a stop to the bullying on one of the most widely used social media platform, we hope this software will serve as a foundation for future improvements/adaptations.
