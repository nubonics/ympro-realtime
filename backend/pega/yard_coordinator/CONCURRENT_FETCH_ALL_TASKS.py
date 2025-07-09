async def fetch_all_pega_tasks(self):
    logger.info('Beginning concurrent fetch of Pega task data...')

    # Define coroutines for concurrent execution
    async def fetch_and_store_workbasket():
        logger.info('Fetching workbasket data...')
        workbasket_html = await self.fetch_workbasket_data()
        workbasket_data = extract_workbasket_tasks(workbasket_html)
        logger.debug(f'Workbasket data extracted: {workbasket_data}')
        valid_tasks = await validate_and_store_tasks(
            workbasket_data, self.task_store, session_manager=self
        )
        try:
            await self.pubsub.publish("workbasket_update", [t.model_dump() for t in valid_tasks])
        except Exception as e:
            logger.error(f"Failed to publish workbasket update: {e}")
            raise e
        logger.info('Workbasket tasks fetched, validated, and stored successfully.')

    async def update_hostler_summary_if_needed():
        logger.debug('Checking if hostler summary needs to be updated...')
        if not self.updated_hostler_summary and self.login_response_text:
            hostlers_summary = extract_hostler_info(self.login_response_text)
            for hostler in hostlers_summary:
                await self.hostler_store.upsert_hostler(hostler)
            self.updated_hostler_summary = True
            await self.pubsub.publish("hostler_summary_update", hostlers_summary)
        logger.debug('Hostler summary updated successfully.')

    async def fetch_all_hostler_details():
        logger.debug('Fetching hostler details for each base_ref...')
        try:
            hostler_payloads = await asyncio.gather(
                *[fetch_hostler_details(self, base_ref=base_ref) for base_ref in self.base_refs]
            )
        except Exception as e:
            logger.error(f"Error fetching hostler payloads: {e}")
            raise e
        aggregated_payload = {"hostlers": hostler_payloads}
        logger.debug(f'Aggregated hostler payload:\n{aggregated_payload}')
        await self.pubsub.publish("hostler_update", aggregated_payload)
        self.last_broadcast_payload = aggregated_payload
        logger.info('Hostler details fetched and broadcasted successfully.')

    # Run all three concurrently
    await asyncio.gather(
        fetch_and_store_workbasket(),
        update_hostler_summary_if_needed(),
        fetch_all_hostler_details()
    )